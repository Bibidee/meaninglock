from pathlib import Path
import pytest
import importlib.util

_HAS_GENLAYER_IMPORT = importlib.util.find_spec('genlayer') is not None

def _contract_type():
    spec = importlib.util.spec_from_file_location('meaning_lock_under_test', 'contracts/meaning_lock.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.MeaningLock, module

def test_contract_isolation():
    assert (Path('contracts') / 'meaning_lock.py').is_file()
    assert len(list(Path('contracts').glob('*.py'))) == 1

def test_core_invariants_are_present():
    source = Path('contracts/meaning_lock.py').read_text(encoding='utf-8')
    assert 'def _send_gen' in source
    assert source.count('emit_transfer') == 1
    assert 'gl.vm.run_nondet_unsafe' in source

def test_lifecycle_and_round_guards_are_present():
    source = Path('contracts/meaning_lock.py').read_text(encoding='utf-8')
    assert 'def claim_uncontested_expiry' in source
    assert 'policy frozen after first challenge' in source
    assert 'review round expired; covenant remains monitorable' in source
    assert 'challenge bond returned' in source

def test_hardened_external_inputs_are_present():
    source = Path('contracts/meaning_lock.py').read_text(encoding='utf-8')
    for marker in ('MAX_URL_CHARS', 'MAX_EVIDENCE_REFERENCES', 'HTTPS URL required', 'HTTPS image URL required', 'digest must be 64 hex characters'):
        assert marker in source

def test_collision_safe_namespaces_and_explicit_debit_source():
    source = Path('contracts/meaning_lock.py').read_text(encoding='utf-8')
    assert '_evidence_key_for' in source and '_audit_key_for' in source
    assert 'source:u256=u256(1)' in source
    assert 'source == u256(2)' in source

def test_appeal_window_is_enforced():
    source = Path('contracts/meaning_lock.py').read_text(encoding='utf-8')
    assert 'appeal window closed' in source
    assert 'appeal window still open' in source
    assert 'self.appeal_deadline[covenant_id]' in source and 'covenant_challenge_window' in source

@pytest.mark.skipif(not _HAS_GENLAYER_IMPORT, reason='GenLayer SDK module is injected by Direct Mode, not exposed to plain pytest imports')
def test_canonical_categories_are_closed_and_deterministic():
    contract_type, module = _contract_type()
    contract = contract_type.__new__(contract_type)
    assert contract._outcome('PRESERVED') == module.PRESERVED
    assert contract._outcome('MATERIAL_CHANGE') == module.CHANGED
    assert contract._outcome('REMOVED') == module.REMOVED
    assert contract._outcome('anything else') == module.UNVERIFIABLE
    assert contract._impact('CRITICAL') == module.CRITICAL
    assert contract._confidence('HIGH') == module.HIGH
    assert contract._mask('255') == module.u256(255)
    assert contract._mask('999') == module.u256(0)

@pytest.mark.skipif(not _HAS_GENLAYER_IMPORT, reason='GenLayer SDK module is injected by Direct Mode, not exposed to plain pytest imports')
def test_verdict_derivation_has_safe_unverifiable_fallback():
    contract_type, module = _contract_type()
    contract = contract_type.__new__(contract_type)
    assert contract._derive({'outcome': module.PRESERVED, 'impact': module.NO_IMPACT, 'confidence': module.HIGH, 'mask': module.u256(0)}) == module.PRESERVED
    assert contract._derive({'outcome': module.CHANGED, 'impact': module.MATERIAL, 'confidence': module.HIGH, 'mask': module.u256(1)}) == module.CHANGED
    assert contract._derive({'outcome': module.PRESERVED, 'impact': module.MATERIAL, 'confidence': module.LOW, 'mask': module.u256(1)}) == module.UNVERIFIABLE


def test_constructor_deploys_in_direct_mode(direct_deploy):
    contract = direct_deploy('contracts/meaning_lock.py', 1, 60, 120)
    assert contract.count == 0


def test_multimodal_evidence_uses_mocked_render_and_json_llm(direct_vm, direct_deploy):
    """Exercise Direct Mode web text, screenshots, and structured LLM output."""
    contract = direct_deploy('contracts/meaning_lock.py', 1, 60, 120)
    direct_vm.mock_web(r"https://.*", {"status": 200, "body": "covenant evidence"})
    direct_vm.mock_llm(r".*Classify only material covenant meaning.*", '{"outcome":"PRESERVED","impact":"NONE","confidence":"HIGH","mask":"0"}')
    record = contract._evidence(
        "https://live.example", "https://baseline.example", "https://baseline.example/image.png",
        "https://evidence.example", "https://evidence.example/image.png",
        "Keep the published terms", "terms", "review"
    )
    assert record["outcome"] == 1  # PRESERVED
    assert record["confidence"] == 2  # HIGH


def _register(contract, vm, publisher, beneficiary, expires=2000000000):
    vm.sender = publisher
    vm.value = 100
    return contract.register_covenant(
        "demo", "https://live.example", "https://baseline.example", "",
        "Keep the published terms", "terms", beneficiary, expires
    )


def _mock_verdict(vm, outcome):
    vm.mock_web(r"https://.*", {"status": 200, "body": "covenant evidence"})
    vm.mock_llm(r".*Classify only material covenant meaning.*", '{"outcome":"%s","impact":"MATERIAL","confidence":"HIGH","mask":"1"}' % outcome)


def test_adverse_review_clears_round_and_blocks_claim_until_appeal_ends(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = direct_deploy('contracts/meaning_lock.py', 1, 60, 120)
    covenant = _register(contract, direct_vm, direct_alice, direct_bob)
    direct_vm.sender = direct_bob
    direct_vm.value = 1
    contract.challenge(covenant, "terms changed", "https://evidence.example", "")
    _mock_verdict(direct_vm, "MATERIAL_CHANGE")
    assert contract.verify(covenant) == 2
    assert contract.get_review_type(covenant) == 0
    assert contract.get_status(covenant)[0] == 3
    with direct_vm.expect_revert("appeal window still open"):
        contract.claim_adverse(covenant)
    direct_vm.warp("2030-01-01T00:00:00Z")
    # The covenant expiry is intentionally far enough away for the appeal
    # grace period to elapse while the covenant remains live.
    assert contract.is_claimable(covenant) is True


def test_unverifiable_review_requires_deadline_then_recovers(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = direct_deploy('contracts/meaning_lock.py', 1, 60, 120)
    covenant = _register(contract, direct_vm, direct_alice, direct_bob)
    direct_vm.sender = direct_bob
    direct_vm.value = 1
    contract.challenge(covenant, "evidence unavailable", "https://evidence.example", "")
    _mock_verdict(direct_vm, "UNVERIFIABLE")
    assert contract.verify(covenant) == 4
    assert contract.get_review_type(covenant) == 0
    assert contract.get_status(covenant)[0] == 3
    with direct_vm.expect_revert("unverifiable recovery unavailable"):
        contract.recover_unverifiable(covenant)
    direct_vm.warp("2030-01-01T00:00:00Z")
    contract.recover_unverifiable(covenant)
    assert contract.get_status(covenant)[0] == 4
    assert contract.get_status(covenant)[4] == 0

from pathlib import Path
import sys
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


@pytest.mark.skipif(sys.platform == 'win32', reason='GenLayer Direct Mode loader has a Windows tempfile-handle lock before contract execution')
def test_constructor_deploys_in_direct_mode(direct_deploy):
    contract = direct_deploy('contracts/meaning_lock.py', args=[1, 60, 120])
    assert contract.count == 0

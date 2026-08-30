import os
import subprocess
from pathlib import Path
import pytest

RPC = os.getenv("MEANINGLOCK_RPC", "https://studio.genlayer.com/api")
ADDRESS = os.getenv("MEANINGLOCK_ADDRESS")
CLI = Path(__file__).parents[2] / "work" / "genlayer-cli" / "node_modules" / "genlayer" / "dist" / "index.js"


def _live_call(method, *args):
    command = ["node", str(CLI), "call", "--rpc", RPC, ADDRESS, method]
    if args:
        command += ["--args", *map(str, args)]
    result = subprocess.run(
        command,
        capture_output=True, text=True, check=True,
    )
    return result.stdout


@pytest.mark.skipif(not ADDRESS, reason="MEANINGLOCK_ADDRESS not supplied")
def test_live_protocol_and_contract_reads():
    assert ADDRESS.startswith("0x") and CLI.is_file()
    protocol = _live_call("get_protocol_config")
    assert "86400" in protocol and "1000000000000000000" in protocol
    # A second ABI read proves schema routing beyond an address-format check.
    if os.getenv("MEANINGLOCK_COVENANT_ID"):
        status = _live_call("get_status", os.environ["MEANINGLOCK_COVENANT_ID"])
        assert "Result:" in status
    else:
        windows = _live_call("get_covenant_windows", "1")
        assert "Result:" in windows or "unknown covenant" in windows.lower()

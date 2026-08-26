import os
import pytest

@pytest.mark.skipif(not os.getenv('MEANINGLOCK_ADDRESS'), reason='deployment address not supplied')
def test_live_address_is_configured():
    assert os.environ['MEANINGLOCK_ADDRESS'].startswith('0x')

import pytest

def mysqrt(y):
    if y < 0:
        raise ValueError("mysqrt(); argument must be non-negative.")
    return 0

def test_mysqrt():
    assert mysqrt(0) == 0
    with pytest.raises(ValueError):
        mysqrt(-1)
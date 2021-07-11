import pytest

from check_url import usage

def test_usage_1():
    argv = []
    assert usage(argv) == True


from spack_commands import time_format

def test_example():
    assert time_format(0.123) == "0.12s"
    assert time_format(123.456) == "2m 3.46s"
    assert time_format(123456.789) == "34h 17m 36.79s"

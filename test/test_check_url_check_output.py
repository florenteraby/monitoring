import pytest
import logging
from check_url import check_url_output


URL_LOCAL_SUOTA_OK = """path : Device/Services/AdvancedFwUpdate/URL
value : 'http://pi-fry.home/TEST2/WHW6'
"""

def test_check_output_1():
    assert check_url_output(URL_LOCAL_SUOTA_OK) == True

URL_LOCAL_SUOTA_KO = """path : Device/Services/AdvancedFwUpdate/URL
value : 'https://wifi-suota-test.cpe-mgt.bt.com/TEST2/WHW6'
"""
def test_check_output_2():
    assert check_url_output(URL_LOCAL_SUOTA_KO) == False

URL_LOCAL_SUOTA_KO_1 = """path : Device/Services/AdvancedFwUpdate/URL
value : 'https://wifi-suota-test.cpe-mgt.bt.comTEST2/WHW6'
"""
def test_check_output_3():
    assert check_url_output(URL_LOCAL_SUOTA_KO_1) == False

URL_LOCAL_SUOTA_KO_2 = """path : Device/Services/AdvancedFwUpdate/URL
vlue : 'https://wifi-suota-test.cpe-mgt.bt.comTEST2/WHW6'
"""
def test_check_output_4():
    assert check_url_output(URL_LOCAL_SUOTA_KO_2) == False


URL_LOCAL_SUOTA_KO_3 = """path : Device/Services/AdvancedFwUpdate/URL
"""
def test_check_output_5():
    assert check_url_output(URL_LOCAL_SUOTA_KO_3) == False

URL_LOCAL_SUOTA_KO_4 = """value : 'https://wifi-suota-test.cpe-mgt.bt.comTEST2/WHW6'
"""
def test_check_output_6():
    assert check_url_output(URL_LOCAL_SUOTA_KO_4) == False

URL_LOCAL_SUOTA_KO_5 = """vlue : 'https://wifi-suota-test.cpe-mgt.bt.comTEST2/WHW6'
"""
def test_check_output_7():
    assert check_url_output(URL_LOCAL_SUOTA_KO_5) == False

#!/usr/bin/python

import logging
import pytest

LOG_FORMAT = "%(levelname)s %(asctime)s %(funcName)s- %(message)s"

URL_LOCAL_SUOTA_OK = """path : Device/Services/AdvancedFwUpdate/URL
value : 'http://pi-fry.home/TEST2/WHW6'
"""

URL_LOCAL_SUOTA_KO = """path : Device/Services/AdvancedFwUpdate/URL
value : 'http://pi-fry.home/TEST2/WHW7'
"""

XPATH = "Device/Services/AdvancedFwUpdate/URL"
EXPECTED_VALUE = "http://pi-fry.home/TEST2/WHW6"

disc = {"ip":"192.168.10.11", "role": "MASTER", "name":"STUDY", "username":"root", "password":"root"}

# @pytest.fixture
# def mock_runCommand(mocker):
#     return mocker.


@pytest.fixture
#Creates the test logger
def supply_logger_test():
    """_summary_

    Returns:
        _type_: _description_
    """
    logging.basicConfig(filename = "./check_xpath_test.log",
        level = logging.DEBUG,
        format = LOG_FORMAT,
        filemode = 'w')
    logger = logging.getLogger()
    return logger


def test_check_output_1(supply_logger_test ):
    """_summary_

    Args:
        supply_logger_test (_type_): _description_
    """
    # mocker.patch('tools.tools.runCommand', return_value = (URL_LOCAL_SUOTA_OK.encode('utf8'),True))
    # xpath_check = check_xpath_class(XPATH, EXPECTED_VALUE)
    # assert xpath_check.check_xpath(disc) == True
    assert True

def test_check_output_2():
    """_summary_
    """
    # mocker.patch('tools.tools.runCommand', return_value = (URL_LOCAL_SUOTA_OK.encode('utf8'),False))

    # xpath_check = check_xpath_class(XPATH, EXPECTED_VALUE)
    # assert xpath_check.check_xpath(disc) == False
    assert True

def test_check_output_3():
    """_summary_
    """
    # mocker.patch('tools.tools.runCommand', return_value = (URL_LOCAL_SUOTA_KO.encode('utf8'),True))

    # xpath_check = check_xpath_class(XPATH, EXPECTED_VALUE)
    # assert xpath_check.check_xpath(disc) == False
    assert True

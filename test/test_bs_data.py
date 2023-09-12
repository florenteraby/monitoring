#!/usr/bin/python
# coding: utf-8
"""_summary_

    Returns:
        _type_: _description_
"""

import logging
import pytest

from bs_data import parse_bs_data

LOG_FORMAT = "%(levelname)s %(asctime)s %(funcName)s- %(message)s"

@pytest.fixture
#Creates the default cermony files
def supply_logger():
    """_summary_

    Args:
        supply_logger (_type_): _description_
    """

    logging.basicConfig(filename = "monitoring_test.log",
    level = logging.INFO,
    format = LOG_FORMAT,
    filemode = 'w')

    logger = logging.getLogger()
    return logger

BS_DATA_OUTPUT_1 = """
  Station Address   PHY Mbps  Data Mbps    Air Use   Data Use    Retries    bw   mcs   Nss   ofdma mu-mimo 
DA:56:05:7B:FD:2B     1200.9        0.0       0.0%      30.5%       0.0%    80    11     2    0.0%    0.0% 
50:84:92:F1:1A:44     1200.9        0.0       0.1%      69.5%       0.0%    80    11     2    0.0%    0.0% 
        (overall)          -        0.0       0.1%         -         -
"""

def test_bs_data_1(supply_logger):
    """_summary_

    Args:
        supply_logger (_type_): _description_
    """
    bs_data = parse_bs_data(BS_DATA_OUTPUT_1, supply_logger)
    assert len(bs_data) == 2
    assert bs_data[0]['station'] == "DA:56:05:7B:FD:2B"
    assert bs_data[0]['retries'] == 0.0
    assert bs_data[1]['station'] == "50:84:92:F1:1A:44"
    assert bs_data[1]['retries'] == 0.0

BS_DATA_OUTPUT_2 = """
  Station Address   PHY Mbps  Data Mbps    Air Use   Data Use    Retries    bw   mcs   Nss   ofdma mu-mimo 
DA:56:05:7B:FD:2B     1200.9        0.0       0.0%      30.5%       15.0%    80    11     2    0.0%    0.0% 
50:84:92:F1:1A:44     1200.9        0.0       0.1%      69.5%       1.0%    80    11     2    0.0%    0.0% 
        (overall)          -        0.0       0.1%         -         -
"""

def test_bs_data_2(supply_logger):
    """_summary_

    Args:
        supply_logger (_type_): _description_
    """
    bs_data = parse_bs_data(BS_DATA_OUTPUT_2, supply_logger)
    assert len(bs_data) == 2
    assert bs_data[0]['station'] == "DA:56:05:7B:FD:2B"
    assert bs_data[0]['phy_mbps'] == 1200.9
    assert bs_data[0]['data_mbps'] == 0.0
    assert bs_data[0]['air_use'] == 0.0
    assert bs_data[0]['data_use'] == 30.5
    assert bs_data[0]['retries'] == 15.0
    assert bs_data[0]['bandwidth'] == 80
    assert bs_data[0]['mcs'] == 11
    assert bs_data[0]['nss'] == 2
    assert bs_data[1]['station'] == "50:84:92:F1:1A:44"
    assert bs_data[1]['phy_mbps'] == 1200.9
    assert bs_data[1]['data_mbps'] == 0.0
    assert bs_data[1]['air_use'] == 0.1
    assert bs_data[1]['data_use'] == 69.5
    assert bs_data[1]['retries'] == 1.0
    assert bs_data[1]['bandwidth'] == 80
    assert bs_data[1]['mcs'] == 11
    assert bs_data[1]['nss'] == 2

BS_DATA_OUTPUT_3 = """
  Station Address   PHY Mbps  Data Mbps    Air Use   Data Use    Retries    bw   mcs   Nss   ofdma mu-mimo 
DA:56:05:7B:FD:2B     1200.9        0.0       0.0%      AA.5%       15.0%    80    11     2    0.0%    0.0% 
50:84:92:F1:1A:44     BBBHH        0.0       0.1%      69.5%       1.0%    80    11     2    0.0%    0.0% 
        (overall)          -        0.0       0.1%         -         -
"""

def test_bs_data_3(supply_logger):
    """_summary_

    Args:
        supply_logger (_type_): _description_
    """
    bs_data = parse_bs_data(BS_DATA_OUTPUT_3, supply_logger)
    assert len(bs_data) == 2
    assert bs_data[0]['station'] == "DA:56:05:7B:FD:2B"
    assert bs_data[0]['phy_mbps'] == 1200.9
    assert bs_data[0]['data_mbps'] == 0.0
    assert bs_data[0]['air_use'] == 0.0
    assert bs_data[0]['data_use'] == -1
    assert bs_data[0]['retries'] == 15.0
    assert bs_data[0]['bandwidth'] == 80
    assert bs_data[0]['mcs'] == 11
    assert bs_data[0]['nss'] == 2
    assert bs_data[1]['station'] == "50:84:92:F1:1A:44"
    assert bs_data[1]['phy_mbps'] == -1
    assert bs_data[1]['data_mbps'] == 0.0
    assert bs_data[1]['air_use'] == 0.1
    assert bs_data[1]['data_use'] == 69.5
    assert bs_data[1]['retries'] == 1.0
    assert bs_data[1]['bandwidth'] == 80
    assert bs_data[1]['mcs'] == 11
    assert bs_data[1]['nss'] == 2

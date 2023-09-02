#!/usr/bin/python
# coding: utf-8
"""_summary_

    Returns:
        _type_: _description_
"""

import logging
import pytest

from pktq_stats import parse_pktq_stats

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

PKTQ_STATS_OUTPUT_1 = """
common queue
prec:(AC)    rqstd,  stored, dropped, retried, rtsfail,rtrydrop, psretry,    acked,utlsn,data Mbits, phy Mbits,%nss 1/2/3/4,  %air, %effcy  (v6)
  00: BK         0,       0,       0,       0,       0,       0,       0,        0,    0,      0.00,      0.00,  -/ -/ -/ -,   0.0,    0.0
  01: BK         0,       0,       0,       -,       -,       0,       0,        0,    0,         -,         -,           -,     -,      -
  02: BK         0,       0,       0,       0,       0,       0,       0,        0,    0,      0.00,      0.00,  -/ -/ -/ -,   0.0,    0.0
  03: BK         0,       0,       0,       -,       -,       0,       0,        0,    0,         -,         -,           -,     -,      -
  04: BE    285087,  285087,       0,       0,       0,       0,       0,        0,   56,      0.00,      0.00,  -/ -/ -/ -,   0.0,    0.0
  05: BE         0,       0,       0,       -,       -,       0,       0,        0,    0,         -,         -,           -,     -,      -
  06: BE         0,       0,       0,       0,       0,       0,       0,        0,    0,      0.00,      0.00,  -/ -/ -/ -,   0.0,    0.0
  07: BE         0,       0,       0,       -,       -,       0,       0,        0,    0,         -,         -,           -,     -,      -
  08: VI         0,       0,       0,       0,       0,       0,       0,        0,    0,      0.00,      0.00,  -/ -/ -/ -,   0.0,    0.0
  09: VI         0,       0,       0,       -,       -,       0,       0,        0,    0,         -,         -,           -,     -,      -
  10: VI         0,       0,       0,       0,       0,       0,       0,        0,    0,      0.00,      0.00,  -/ -/ -/ -,   0.0,    0.0
  11: VI         0,       0,       0,       -,       -,       0,       0,        0,    0,         -,         -,           -,     -,      -
  12: VO    230157,  230157,       0,       0,       0,       0,       0,        0,    2,      0.00,      0.00,  -/ -/ -/ -,   0.0,    0.0
  13: VO         0,       0,       0,       -,       -,       0,       0,        0,    0,         -,         -,           -,     -,      -
  14: VO         0,       0,       0,      42,       0,       6,       0,        1,    0,      0.00,      6.00,  -/ -/ -/ -,   0.0,    1.9
  15: VO        60,      60,       0,       -,       -,       0,       0,        0,    0,         -,         -,           -,     -,      -
"""
def test_pktq_stats_1(supply_logger):
    """_summary_

    Args:
        supply_logger (_type_): _description_
    """
    queue = parse_pktq_stats(PKTQ_STATS_OUTPUT_1, supply_logger)
    assert len(queue) == 16
    assert queue[0].get('BK').get("STATS").get("queue") == "bk"
    assert queue[0].get('BK').get("STATS").get("retried") == 0
    assert queue[9].get('VI').get("STATS").get("retried") == -1
    assert queue[14].get('VO').get("STATS").get("queue") == "vo"
    assert queue[14].get('VO').get("STATS").get("retried") == 42
    assert queue[14].get('VO').get("STATS").get("rtrydrop") == 6

PKTQ_STATS_OUTPUT_2 = """
common queue
prec:(AC)    rqstd,  stored, dropped, retried, rtsfail,rtrydrop, psretry,    acked,utlsn,data Mbits, phy Mbits,%nss 1/2/3/4,  %air, %effcy  (v6)

"""
def test_pktq_stats_2(supply_logger):
    """_summary_

    Args:
        supply_logger (_type_): _description_
    """
    queue = parse_pktq_stats(PKTQ_STATS_OUTPUT_2, supply_logger)
    assert len(queue) == 0

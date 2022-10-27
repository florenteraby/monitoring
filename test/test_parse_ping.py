import pytest
import logging
from monitor import parse_ping_wodns

LOG_FORMAT = "%(levelname)s %(asctime)s %(funcName)s- %(message)s"

@pytest.fixture
#Creates the default cermony files
def supply_logger():
    logging.basicConfig(filename = "monitoring_test.log",
    level = logging.INFO,
    format = LOG_FORMAT,
    filemode = 'w')

    logger = logging.getLogger()
    return logger

ping_result_ok = """PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: seq=0 ttl=115 time=13.199 ms

--- 8.8.8.8 ping statistics ---
1 packets transmitted, 1 packets received, 0% packet loss
round-trip min/avg/max = 13.199/13.199/13.199 ms"""

ping_result_ko = """PING 255.255.255.255 (255.255.255.255): 56 data bytes

--- 255.255.255.255 ping statistics ---
1 packets transmitted, 0 packets received, 100% packet loss
"""
def test_parse_ping_OK(supply_logger):
    round_trip = parse_ping_wodns(ping_result_ok)
    assert round_trip == 13.199

def test_parse_ping_KO(supply_logger):
    round_trip = parse_ping_wodns(ping_result_ko)
    assert round_trip == -1.0
    assert type(round_trip) == float



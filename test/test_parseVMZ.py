import pytest
import os
import logging
from monitor import parseProcessVMZ 

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


output_hg6d_2 = """17098 root      3244 R    grep -w hg6d
1202 root     43168 S    hg6d
"""
output_hg6d_6 = """17098 root      3244 R    grep -w hg6d
1202 root     43168 S    hg6d
"""

output_hg6d_10 = """17098 root      3244 R    grep -w hg6d
1202 root     43168 R    hg6d
"""

output_hg6d_7 = """17098 root      3244 R    grep -w hg6d
1202 root     143m S    hg6d
"""

output_hg6d_8 = """17098 root      3244 R    grep -w hg6d
1202 root     143m R    hg6d
"""

output_hg6d_1 = """1202 root     43168 S    hg6d
17098 root      3244 R    grep -w hg6d
"""
output_hg6d_5 = """1202 root     43168 S    hg6d
17098 root      3244 S    grep -w hg6d
"""

output_hg6d_9 = """1202 root     43168 R    hg6d
17098 root      3244 S    grep -w hg6d
"""

output_hg6d_3 = """1202 root     143m S    hg6d
17098 root      3244 R    grep -w hg6d
"""
output_hg6d_4 = """1202 root     143m R    hg6d
17098 root      3244 R    grep -w hg6d
"""

output_hg6d_11 = """17098 root      3244 R    grep -w hg6d
"""

output_hg6d_12 = """17098 root      3244 S    grep -w hg6d
"""


def test_parseHG6D_1(supply_logger):
    vmz = parseProcessVMZ("hg6d", output_hg6d_1, supply_logger)
    assert vmz == 43168

def test_parseHG6D_2(supply_logger):
    vmz = parseProcessVMZ("hg6d", output_hg6d_2, supply_logger)
    assert vmz == 43168


def test_parseHG6D_3(supply_logger):
    vmz = parseProcessVMZ("hg6d", output_hg6d_3, supply_logger)
    assert vmz == 143000000

def test_parseHG6D_4(supply_logger):
    vmz = parseProcessVMZ("hg6d", output_hg6d_4, supply_logger)
    assert vmz == 143000000

def test_parseHG6D_5(supply_logger):
    vmz = parseProcessVMZ("hg6d", output_hg6d_5, supply_logger)
    assert vmz == 43168

def test_parseHG6D_6(supply_logger):
    vmz = parseProcessVMZ("hg6d", output_hg6d_6, supply_logger)
    assert vmz == 43168

def test_parseHG6D_7(supply_logger):
    vmz = parseProcessVMZ("hg6d", output_hg6d_7, supply_logger)
    assert vmz == 143000000

def test_parseHG6D_8(supply_logger):
    vmz = parseProcessVMZ("hg6d", output_hg6d_8, supply_logger)
    assert vmz == 143000000

def test_parseHG6D_9(supply_logger):
    vmz = parseProcessVMZ("hg6d", output_hg6d_9, supply_logger)
    assert vmz == 43168

def test_parseHG6D_10(supply_logger):
    vmz = parseProcessVMZ("hg6d", output_hg6d_10, supply_logger)
    assert vmz == 43168

def test_parseHG6D_11(supply_logger):
    vmz = parseProcessVMZ("hg6d", output_hg6d_11, supply_logger)
    assert vmz == -1

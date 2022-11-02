#!/usr/bin/python

import pytest
import os
from monitor import parse_BH_assoclist

BH_2_ENTRIES_ANSWER =  """assoclist 80:20:DA:EE:89:A7
assoclist E8:AD:A6:EA:1D:B1
"""
BH_1_ENTRIES_ANSWER =  """assoclist 10:D7:B0:1A:96:6F
"""
BH_3_ENTRIES_ANSWER =  """assoclist 10:D7:B0:1A:96:6F
assoclist 10:D7:B0:1A:96:7B
assoclist 10:D7:B0:1A:96:7B
"""


def test_parse_bh_empty_answer():
    to_parse = ""
    command_type = "WIFI_BH_ASSOCLIST"
    row = {}
    success_command = True

    my_list = parse_BH_assoclist(to_parse, row, command_type, success_command)
    for STA in my_list:
        macSta = STA.split(" ")[1]
        assert macSta in ["80:20:DA:EE:89:A7", "E8:AD:A6:EA:1D:B1", "10:D7:B0:1A:96:6F", "10:D7:B0:1A:96:7B"]
    assert row['WIFI_BH_ASSOCLIST'] == 0
    assert len(my_list) == 0

def test_parse_bh_entries_answer():
    to_parse = BH_1_ENTRIES_ANSWER
    command_type = "WIFI_BH_ASSOCLIST"
    row = {}
    success_command = True

    my_list = parse_BH_assoclist(to_parse, row, command_type, success_command)
    assert row['WIFI_BH_ASSOCLIST'] == 1
    assert len(my_list) != 0
    ONE_ANSWER = BH_1_ENTRIES_ANSWER.split("\n")
    del ONE_ANSWER[-1]
    assert my_list == ONE_ANSWER
    for STA in my_list:
        mac_sta = STA.split(" ")[1]
        assert mac_sta in ["80:20:DA:EE:89:A7", "E8:AD:A6:EA:1D:B1", "10:D7:B0:1A:96:6F", "10:D7:B0:1A:96:7B"]

def test_parse_bh_2_entries_answer():
    to_parse = BH_2_ENTRIES_ANSWER
    command_type = "WIFI_BH_ASSOCLIST"
    row = {}
    success_command = True

    my_list = parse_BH_assoclist(to_parse, row, command_type, success_command)
    assert row['WIFI_BH_ASSOCLIST'] == 2
    assert len(my_list) != 0
    ONE_ANSWER = BH_2_ENTRIES_ANSWER.split("\n")
    del ONE_ANSWER[-1]
    assert my_list == ONE_ANSWER
    for STA in my_list:
        mac_sta = STA.split(" ")[1]
        assert mac_sta in ["80:20:DA:EE:89:A7", "E8:AD:A6:EA:1D:B1", "10:D7:B0:1A:96:6F", "10:D7:B0:1A:96:7B"]

def test_parse_bh_3_entries_answer():
    to_parse = BH_3_ENTRIES_ANSWER
    command_type = "WIFI_BH_ASSOCLIST"
    row = {}
    success_command = True

    my_list = parse_BH_assoclist(to_parse, row, command_type, success_command)
    assert row['WIFI_BH_ASSOCLIST'] == 3
    assert len(my_list) != 0
    ONE_ANSWER = BH_3_ENTRIES_ANSWER.split("\n")
    del ONE_ANSWER[-1]
    assert my_list == ONE_ANSWER
    for STA in my_list:
        mac_sta = STA.split(" ")[1]
        assert mac_sta in ["80:20:DA:EE:89:A7", "E8:AD:A6:EA:1D:B1", "10:D7:B0:1A:96:6F", "10:D7:B0:1A:96:7B"]

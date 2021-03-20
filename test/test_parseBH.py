import pytest
import os
from monitor import parseBHAssoclist

BH2ENTRIESANSWER =  """assoclist 80:20:DA:EE:89:A7
assoclist E8:AD:A6:EA:1D:B1
"""
BH1ENTRIESANSWER =  """assoclist 10:D7:B0:1A:96:6F
"""
BH3ENTRIESANSWER =  """assoclist 10:D7:B0:1A:96:6F
assoclist 10:D7:B0:1A:96:7B
assoclist 10:D7:B0:1A:96:7B
"""


def test_parseBHEmptyAnswer():
    to_parse = ""
    command_type = "WIFI_BH_ASSOCLIST"
    row = {}
    success_command = True

    myList = parseBHAssoclist(to_parse, row, command_type, success_command)
    for STA in myList:
        macSta = STA.split(" ")[1]
        assert macSta in ["80:20:DA:EE:89:A7", "E8:AD:A6:EA:1D:B1", "10:D7:B0:1A:96:6F", "10:D7:B0:1A:96:7B"]
    assert row['WIFI_BH_ASSOCLIST'] == 0
    assert len(myList) == 0

def test_parseBH1EntriesAnswer():
    to_parse = BH1ENTRIESANSWER
    command_type = "WIFI_BH_ASSOCLIST"
    row = {}
    success_command = True

    myList = parseBHAssoclist(to_parse, row, command_type, success_command)
    assert row['WIFI_BH_ASSOCLIST'] == 1
    assert len(myList) != 0
    ONEANSWER = BH1ENTRIESANSWER.split("\n")
    del ONEANSWER[-1]
    assert myList == ONEANSWER
    for STA in myList:
        macSta = STA.split(" ")[1]
        assert macSta in ["80:20:DA:EE:89:A7", "E8:AD:A6:EA:1D:B1", "10:D7:B0:1A:96:6F", "10:D7:B0:1A:96:7B"]

def test_parseBH2EntriesAnswer():
    to_parse = BH2ENTRIESANSWER
    command_type = "WIFI_BH_ASSOCLIST"
    row = {}
    success_command = True

    myList = parseBHAssoclist(to_parse, row, command_type, success_command)
    assert row['WIFI_BH_ASSOCLIST'] == 2
    assert len(myList) != 0
    ONEANSWER = BH2ENTRIESANSWER.split("\n")
    del ONEANSWER[-1]
    assert myList == ONEANSWER
    for STA in myList:
        macSta = STA.split(" ")[1]
        assert macSta in ["80:20:DA:EE:89:A7", "E8:AD:A6:EA:1D:B1", "10:D7:B0:1A:96:6F", "10:D7:B0:1A:96:7B"]

def test_parseBH3EntriesAnswer():
    to_parse = BH3ENTRIESANSWER
    command_type = "WIFI_BH_ASSOCLIST"
    row = {}
    success_command = True

    myList = parseBHAssoclist(to_parse, row, command_type, success_command)
    assert row['WIFI_BH_ASSOCLIST'] == 3
    assert len(myList) != 0
    ONEANSWER = BH3ENTRIESANSWER.split("\n")
    del ONEANSWER[-1]
    assert myList == ONEANSWER
    for STA in myList:
        macSta = STA.split(" ")[1]
        assert macSta in ["80:20:DA:EE:89:A7", "E8:AD:A6:EA:1D:B1", "10:D7:B0:1A:96:6F", "10:D7:B0:1A:96:7B"]

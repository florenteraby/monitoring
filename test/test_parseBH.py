import pytest
import os
from monitor import parseBHAssoclist

BH2ENTRIESANSWER =  "assoclist 10:D7:B0:1A:96:6F\nassoclist 10:D7:B0:1A:96:7B\n"
BH1ENTRIESANSWER =  "assoclist 10:D7:B0:1A:96:6F\n"
BH3ENTRIESANSWER =  "assoclist 10:D7:B0:1A:96:6F\nassoclist 10:D7:B0:1A:96:7B\nassoclist 10:D7:B0:1A:96:7B\n"


def test_parseBHEmptyAnswer():
    to_parse = ""
    command_type = "WIFI_BH_ASSOCLIST"
    row = {}
    success_command = True

    myList = parseBHAssoclist(to_parse, row, command_type, success_command)
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
    assert myList == BH1ENTRIESANSWER.split("\n")

def test_parseBH2EntriesAnswer():
    to_parse = BH2ENTRIESANSWER
    command_type = "WIFI_BH_ASSOCLIST"
    row = {}
    success_command = True

    myList = parseBHAssoclist(to_parse, row, command_type, success_command)
    assert row['WIFI_BH_ASSOCLIST'] == 2
    assert len(myList) != 0
    assert myList == BH2ENTRIESANSWER.split("\n")

def test_parseBH3EntriesAnswer():
    to_parse = BH3ENTRIESANSWER
    command_type = "WIFI_BH_ASSOCLIST"
    row = {}
    success_command = True

    myList = parseBHAssoclist(to_parse, row, command_type, success_command)
    assert row['WIFI_BH_ASSOCLIST'] == 3
    assert len(myList) != 0
    assert myList == BH3ENTRIESANSWER.split("\n")
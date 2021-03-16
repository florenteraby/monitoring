import pytest
import os
from monitor import parseBHAssoclist

BH2ENTRIESANSWER =  "assoclist 10:D7:B0:1A:96:6F\nassoclist 10:D7:B0:1A:96:7B"
BH1ENTRIESANSWER =  "assoclist 10:D7:B0:1A:96:6F"


def test_parseBHEmptyAnswer():
    to_parse = ""
    command_type = "WIFI_BH_ASSOCLIST"
    row = {}
    success_command = True

    parseBHAssoclist(to_parse, row, command_type, success_command)
    assert row['WIFI_BH_ASSOCLIST'] == 0

def test_parseBH1EntriesAnswer():
    to_parse = BH1ENTRIESANSWER
    command_type = "WIFI_BH_ASSOCLIST"
    row = {}
    success_command = True

    parseBHAssoclist(to_parse, row, command_type, success_command)
    assert row['WIFI_BH_ASSOCLIST'] == 1


def test_parseBH2EntriesAnswer():
    to_parse = BH2ENTRIESANSWER
    command_type = "WIFI_BH_ASSOCLIST"
    row = {}
    success_command = True

    parseBHAssoclist(to_parse, row, command_type, success_command)
    assert row['WIFI_BH_ASSOCLIST'] == 2
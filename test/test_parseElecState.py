#!/usr/bin/python


import pytest
from monitor import parse_election_state

SLAVEROOT_OUTPUT = "ElecState <ELECTION_STATE_SLAVEROOT>, MasterState <NO_OPTION_102>, Option 102 <>, GwState<GATEWAY_FOUND>, GwRtrF<0>, MyScore <5>, Buffer <> GwPortFound <true>"
MASTER_OUTPUT = "ElecState <ELECTION_STATE_MASTER>, MasterState <NO_OPTION_102>, Option 102 <>, GwState<GATEWAY_FOUND>, GwRtrF<0>, MyScore <0>, Buffer <+105601+NQ04800383!0> GwPortFound <true>"
SLAVE_OUTPUT = "ElecState <ELECTION_STATE_SLAVE>, MasterState <OPTION_102_WITH_SCORE>, Option 102 <+105601+NQ04800384>, GwState<GATEWAY_FOUND>, GwRtrF<1>, MyScore <-1>, Buffer <> GwPortFound <false>"


def test_parse_elec_state_slave_root():
    """_summary_
    """
    elec_state = parse_election_state(SLAVEROOT_OUTPUT)
    assert elec_state == "ELECTION_STATE_SLAVEROOT"

def test_parse_elec_state_master():
    """_summary_
    """
    elec_state = parse_election_state(MASTER_OUTPUT)
    assert elec_state == "ELECTION_STATE_MASTER"

def test_parse_elec_state_slave():
    """_summary_
    """
    elec_state = parse_election_state(SLAVE_OUTPUT)
    assert elec_state == "ELECTION_STATE_SLAVE"

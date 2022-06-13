import pytest
import os
from monitor import parseElecState

SLAVEROOT_OUTPUT = "ElecState <ELECTION_STATE_SLAVEROOT>, MasterState <NO_OPTION_102>, Option 102 <>, GwState<GATEWAY_FOUND>, GwRtrF<0>, MyScore <5>, Buffer <> GwPortFound <true>"
MASTER_OUTPUT = "ElecState <ELECTION_STATE_MASTER>, MasterState <NO_OPTION_102>, Option 102 <>, GwState<GATEWAY_FOUND>, GwRtrF<0>, MyScore <0>, Buffer <+105601+NQ04800383!0> GwPortFound <true>"
SLAVE_OUTPUT = "ElecState <ELECTION_STATE_SLAVE>, MasterState <OPTION_102_WITH_SCORE>, Option 102 <+105601+NQ04800384>, GwState<GATEWAY_FOUND>, GwRtrF<1>, MyScore <-1>, Buffer <> GwPortFound <false>"


def test_parseElecState_SlaveRoot():
    elecState = parseElecState(SLAVEROOT_OUTPUT)
    assert elecState == "ELECTION_STATE_SLAVEROOT"

def test_parseElecState_Master():
    elecState = parseElecState(MASTER_OUTPUT)
    assert elecState == "ELECTION_STATE_MASTER"

def test_parseElecState_Slave():
    elecState = parseElecState(SLAVE_OUTPUT)
    assert elecState == "ELECTION_STATE_SLAVE"
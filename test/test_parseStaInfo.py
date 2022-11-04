import pytest
from monitor import parse_sta_info

STA_INFO = """[VER 8] STA 10:D7:B0:1A:96:6F:
    chanspec 116/80 (0xe07a)
    aid:13
    rateset [ 6 9 12 18 24 36 48 54 ]
    idle 0 seconds
    in network 13416 seconds
    state: AUTHENTICATED ASSOCIATED AUTHORIZED
    connection: SECURED
    auth: WPA2-PSK
    crypto: AES_CCM
    flags 0x351e03b: BRCM WME N_CAP VHT_CAP HE_CAP AMPDU AMSDU DWDS_CAP DWDS_ACTIVE
    HT caps 0x1ef: LDPC 40MHz SGI20 SGI40 STBC-Tx STBC-Rx
    VHT caps 0xfb: LDPC SGI80 STBC-Tx STBC-Rx SU-BFR SU-BFE MU-BFR
    HE caps 0x6689: LDPC HE-HTC
    OMI 0x00f3: 80Mhz rx=4ss tx=4ss UL_MU_DISABLE 
    TWT info 0x1: CAPABLE
    tx total pkts: 427850
    tx total bytes: 145704772
    tx ucast pkts: 367774
    tx ucast bytes: 139126948
    tx mcast/bcast pkts: 60076
    tx mcast/bcast bytes: 6577824
    tx failures: 11
    rx data pkts: 265829
    rx data bytes: 118666736
    rx data dur: 0
    rx ucast pkts: 252389
    rx ucast bytes: 116006201
    rx mcast/bcast pkts: 13440
    rx mcast/bcast bytes: 2660535
    rate of last tx pkt: 1814790 kbps - 1088880 kbps
    rate of last rx pkt: 1801470 kbps
    rx decrypt succeeds: 265824
    rx decrypt failures: 0
    tx data pkts retried: 2
    per antenna rssi of last rx data frame: -31 -32 -32 -32
    per antenna average rssi of rx data frames: -30 -32 -31 -33
    per antenna noise floor: -93 -93 -90 -93
    tx total pkts sent: 367774
    tx pkts retries: 42782
    tx pkts retry exhausted: 0
    tx FW total pkts sent: 19
    tx FW pkts retries: 1
    tx FW pkts retry exhausted: 0
    rx total pkts retried: 4566
MCS SET : [ 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 ]
VHT SET : 0x1 1x1 2x1 3x1 4x1 5x1 6x1 7x1 8x1 9x1 10x1 11x1 
        : 0x2 1x2 2x2 3x2 4x2 5x2 6x2 7x2 8x2 9x2 10x2 11x2 
        : 0x3 1x3 2x3 3x3 4x3 5x3 6x3 7x3 8x3 9x3 10x3 11x3 
        : 0x4 1x4 2x4 3x4 4x4 5x4 6x4 7x4 8x4 9x4 10x4 11x4 
HE SET  : 
            20/40/80 MHz:
                NSS1 Tx: 0-11        Rx: 0-11 
                NSS2 Tx: 0-11        Rx: 0-11 
                NSS3 Tx: 0-11        Rx: 0-11 
                NSS4 Tx: 0-11        Rx: 0-11 
smoothed rssi: -30 
tx nrate 
he mcs 9 Nss 4 Tx Exp 0 bw80 ldpc 2xLTF GI 1.6us auto
rx nrate
he mcs 11 Nss 3 Tx Exp 0 bw80 ldpc 2xLTF GI 0.8us auto 
wnm
0x1:  BSS-Transition
VENDOR OUI VALUE[0] 00:90:4C 
VENDOR OUI VALUE[1] 00:10:18 
VENDOR OUI VALUE[2] 00:50:F2 
link bandwidth = 80 MHZ 
RRM capability = 0x32  Neighbor_Report Beacon_Passive Beacon_Active
"""

def test_parse_sta_info():
    """_summary_
    """
    row = {}
    mac_sta = "10:D7:B0:1A:96:6F"
    row = parse_sta_info(STA_INFO, mac_sta)
    assert row['BH_STA_INFO_TX_FAILURES_'+mac_sta] == 11
    assert row['BH_STA_INFO_BANDWIDTH_'+mac_sta] == 80
    assert row['BH_STA_INFO_UPTIME_'+mac_sta] == 13416
    assert row['BH_STA_INFO_DECRYPT_FAILURE_'+mac_sta] == 0

def test_parse_sta_info_empty():
    """ _summary_
    """
    row = {}
    mac_sta = "10:D7:B0:1A:96:6F"
    row = parse_sta_info("", mac_sta)
    assert len(row) == 0

STA_INFO_MISSING_BANDWIDTH = """[VER 8] STA 10:D7:B0:1A:96:6F:
    chanspec 116/80 (0xe07a)
    aid:13
    rateset [ 6 9 12 18 24 36 48 54 ]
    idle 0 seconds
    in network 13416 seconds
    state: AUTHENTICATED ASSOCIATED AUTHORIZED
    connection: SECURED
    auth: WPA2-PSK
    crypto: AES_CCM
    flags 0x351e03b: BRCM WME N_CAP VHT_CAP HE_CAP AMPDU AMSDU DWDS_CAP DWDS_ACTIVE
    HT caps 0x1ef: LDPC 40MHz SGI20 SGI40 STBC-Tx STBC-Rx
    VHT caps 0xfb: LDPC SGI80 STBC-Tx STBC-Rx SU-BFR SU-BFE MU-BFR
    HE caps 0x6689: LDPC HE-HTC
    OMI 0x00f3: 80Mhz rx=4ss tx=4ss UL_MU_DISABLE 
    TWT info 0x1: CAPABLE
    tx total pkts: 427850
    tx total bytes: 145704772
    tx ucast pkts: 367774
    tx ucast bytes: 139126948
    tx mcast/bcast pkts: 60076
    tx mcast/bcast bytes: 6577824
    tx failures: 11
    rx data pkts: 265829
    rx data bytes: 118666736
    rx data dur: 0
    rx ucast pkts: 252389
    rx ucast bytes: 116006201
    rx mcast/bcast pkts: 13440
    rx mcast/bcast bytes: 2660535
    rate of last tx pkt: 1814790 kbps - 1088880 kbps
    rate of last rx pkt: 1801470 kbps
    rx decrypt succeeds: 265824
    rx decrypt failures: 0
    tx data pkts retried: 2
    per antenna rssi of last rx data frame: -31 -32 -32 -32
    per antenna average rssi of rx data frames: -30 -32 -31 -33
    per antenna noise floor: -93 -93 -90 -93
    tx total pkts sent: 367774
    tx pkts retries: 42782
    tx pkts retry exhausted: 0
    tx FW total pkts sent: 19
    tx FW pkts retries: 1
    tx FW pkts retry exhausted: 0
    rx total pkts retried: 4566
MCS SET : [ 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 ]
VHT SET : 0x1 1x1 2x1 3x1 4x1 5x1 6x1 7x1 8x1 9x1 10x1 11x1 
        : 0x2 1x2 2x2 3x2 4x2 5x2 6x2 7x2 8x2 9x2 10x2 11x2 
        : 0x3 1x3 2x3 3x3 4x3 5x3 6x3 7x3 8x3 9x3 10x3 11x3 
        : 0x4 1x4 2x4 3x4 4x4 5x4 6x4 7x4 8x4 9x4 10x4 11x4 
HE SET  : 
            20/40/80 MHz:
                NSS1 Tx: 0-11        Rx: 0-11 
                NSS2 Tx: 0-11        Rx: 0-11 
                NSS3 Tx: 0-11        Rx: 0-11 
                NSS4 Tx: 0-11        Rx: 0-11 
smoothed rssi: -30 
tx nrate 
he mcs 9 Nss 4 Tx Exp 0 bw80 ldpc 2xLTF GI 1.6us auto
rx nrate
he mcs 11 Nss 3 Tx Exp 0 bw80 ldpc 2xLTF GI 0.8us auto 
wnm
0x1:  BSS-Transition
VENDOR OUI VALUE[0] 00:90:4C 
VENDOR OUI VALUE[1] 00:10:18 
VENDOR OUI VALUE[2] 00:50:F2 
RRM capability = 0x32  Neighbor_Report Beacon_Passive Beacon_Active
"""


def test_parse_sta_info_missing_param_1():
    """_summary_
    """
    row = {}
    mac_sta = "10:D7:B0:1A:96:6F"
    row = parse_sta_info(STA_INFO_MISSING_BANDWIDTH, mac_sta)
    assert row['BH_STA_INFO_TX_FAILURES_'+mac_sta] == 11
    assert 'BH_STA_INFO_BANDWIDTH_'+mac_sta not in row
    assert row['BH_STA_INFO_UPTIME_'+mac_sta] == 13416
    assert row['BH_STA_INFO_DECRYPT_FAILURE_'+mac_sta] == 0

STA_INFO_UPTIME_FLOAT = """[VER 8] STA 10:D7:B0:1A:96:6F:
    chanspec 116/80 (0xe07a)
    aid:13
    rateset [ 6 9 12 18 24 36 48 54 ]
    idle 0 seconds
    in network 13416333333 seconds
    : AUTHENTICATED ASSOCIATED AUTHORIZED
    ction: SECURED
    WPA2-PSK
    crypto: AES_CCM
    flags 0x351e03b: BRCM WME N_CAP VHT_CAP HE_CAP AMPDU AMSDU DWDS_CAP DWDS_ACTIVE
    HT caps 0x1ef: LDPC 40MHz SGI20 SGI40 STBC-Tx STBC-Rx
    VHT caps 0xfb: LDPC SGI80 STBC-Tx STBC-Rx SU-BFR SU-BFE MU-BFR
    HE caps 0x6689: LDPC HE-HTC
    OMI 0x00f3: 80Mhz rx=4ss tx=4ss UL_MU_DISABLE 
    TWT info 0x1: CAPABLE
    tx total pkts: 427850
    tx total bytes: 145704772
    tx ucast pkts: 367774
    tx ucast bytes: 139126948
    tx mcast/bcast pkts: 60076
    tx mcast/bcast bytes: 6577824
    tx failures: 11
    rx data pkts: 265829
    rx data bytes: 118666736
    rx data dur: 0
    rx ucast pkts: 252389
    rx ucast bytes: 116006201
    rx mcast/bcast pkts: 13440
    rx mcast/bcast bytes: 2660535
    rate of last tx pkt: 1814790 kbps - 1088880 kbps
    rate of last rx pkt: 1801470 kbps
    rx decrypt succeeds: 265824
    rx decrypt failures: 0
    tx data pkts retried: 2
    per antenna rssi of last rx data frame: -31 -32 -32 -32
    per antenna average rssi of rx data frames: -30 -32 -31 -33
    per antenna noise floor: -93 -93 -90 -93
    tx total pkts sent: 367774
    tx pkts retries: 42782
    tx pkts retry exhausted: 0
    tx FW total pkts sent: 19
    tx FW pkts retries: 1
    tx FW pkts retry exhausted: 0
    rx total pkts retried: 4566
MCS  [ 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 ]
VHT  0x1 1x1 2x1 3x1 4x1 5x1 6x1 7x1 8x1 9x1 10x1 11x1 
     0x2 1x2 2x2 3x2 4x2 5x2 6x2 7x2 8x2 9x2 10x2 11x2 
     0x3 1x3 2x3 3x3 4x3 5x3 6x3 7x3 8x3 9x3 10x3 11x3 
     0x4 1x4 2x4 3x4 4x4 5x4 6x4 7x4 8x4 9x4 10x4 11x4 
HE S 
            20/40/80 MHz:
                NSS1 Tx: 0-11        Rx: 0-11 
                NSS2 Tx: 0-11        Rx: 0-11 
                NSS3 Tx: 0-11        Rx: 0-11 
                NSS4 Tx: 0-11        Rx: 0-11 
smoothed rssi: -30 
tx nrate 
he mcs 9 Nss 4 Tx Exp 0 bw80 ldpc 2xLTF GI 1.6us auto
rx nrate
he mcs 11 Nss 3 Tx Exp 0 bw80 ldpc 2xLTF GI 0.8us auto 
wnm
0x1:  BSS-Transition
VENDOR OUI VALUE[0] 00:90:4C 
VENDOR OUI VALUE[1] 00:10:18 
VENDOR OUI VALUE[2] 00:50:F2 
link bandwidth = 80 MHZ 
RRM capability = 0x32  Neighbor_Report Beacon_Passive Beacon_Active
"""
def test_parse_sta_info_missing_param_2():
    """_summary_
    """
    row = {}
    mac_sta = "10:D7:B0:1A:96:6F"
    row = parse_sta_info(STA_INFO_UPTIME_FLOAT, mac_sta)
    assert row['BH_STA_INFO_TX_FAILURES_'+mac_sta] == 11
    assert row['BH_STA_INFO_BANDWIDTH_'+mac_sta] == 80
    assert row['BH_STA_INFO_UPTIME_'+mac_sta] == 13416333333
    assert row['BH_STA_INFO_DECRYPT_FAILURE_'+mac_sta] == 0


SAT_INFO_KO_IN_FILED = """[VER 8] STA 80:20:DA:EE:89:A7:
	 chanspec 136/80 (0xe18a)
	 aid:13 
	 rateset [ 6 9 12 18 24 36 48 54 ]
	 idle 0 seconds
	in network 339317 seconds
	 state: AUTHENTICATED ASSOCIATED AUTHORIZED
	 connection: SECURED
	 auth: WPA2-PSK
	 crypto: AES_CCM
	 flags 0x351e03b: BRCM WME N_CAP VHT_CAP HE_CAP AMPDU AMSDU DWDS_CAP DWDS_ACTIVE
	 HT caps 0x1ef: LDPC 40MHz SGI20 SGI40 STBC-Tx STBC-Rx
	 VHT caps 0xfb: LDPC SGI80 STBC-Tx STBC-Rx SU-BFR SU-BFE MU-BFR
	 HE caps 0x6689: LDPC HE-HTC
	 OMI 0x00f3: 80Mhz rx=4ss tx=4ss UL_MU_DISABLE 
	 TWT info 0x1: CAPABLE
	 tx total pkts: 37389133
	 tx total bytes: 25822979079
	 tx ucast pkts: 34956578
	 tx ucast bytes: 25527817099
	 tx mcast/bcast pkts: 2432555
	 tx mcast/bcast bytes: 295161980
	 tx failures: 6
	 rx data pkts: 26404505
	 rx data bytes: 11580105720
	 rx data dur: 0
	 rx ucast pkts: 25558142
	 rx ucast bytes: 11396502304
	 rx mcast/bcast pkts: 846363
	 rx mcast/bcast bytes: 183603416
	 rate of last tx pkt: 1152940 kbps - 288230 kbps
	 rate of last rx pkt: 864700 kbps
	 rx decrypt succeeds: 26404403
	 rx decrypt failures: 0
	 tx data pkts retried: 3
	 per antenna rssi of last rx data frame: -67 -63 -67 -64
	 per antenna average rssi of rx data frames: -67 -63 -67 -64
	 per antenna noise floor: -91 -92 -91 -91
	 tx total pkts sent: 34956571
	 tx pkts retries: 4086027
	 tx pkts retry exhausted: 6
	 tx FW total pkts sent: 18
	 tx FW pkts retries: 2
	 tx FW pkts retry exhausted: 0
	 rx total pkts retried: 1830689
MCS SET : [ 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 ]
VHT SET : 0x1 1x1 2x1 3x1 4x1 5x1 6x1 7x1 8x1 9x1 10x1 11x1 
        : 0x2 1x2 2x2 3x2 4x2 5x2 6x2 7x2 8x2 9x2 10x2 11x2 
        : 0x3 1x3 2x3 3x3 4x3 5x3 6x3 7x3 8x3 9x3 10x3 11x3 
        : 0x4 1x4 2x4 3x4 4x4 5x4 6x4 7x4 8x4 9x4 10x4 11x4 
HE SET  :
	    20/40/80 MHz:
		NSS1 Tx: 0-11        Rx: 0-11
		NSS2 Tx: 0-11        Rx: 0-11
		NSS3 Tx: 0-11        Rx: 0-11
		NSS4 Tx: 0-11        Rx: 0-11
smoothed rssi: -63
tx nrate
he mcs 5 Nss 4 Tx Exp 0 bw80 ldpc 2xLTF GI 0.8us auto
rx nrate
he mcs 5 Nss 3 Tx Exp 0 bw80 ldpc 2xLTF GI 0.8us auto
wnm
0x1:  BSS-Transition
VENDOR OUI VALUE[0] 00:90:4C 
VENDOR OUI VALUE[1] 00:10:18 
VENDOR OUI VALUE[2] 00:50:F2 
link bandwidth = 80 MHZ 
RRM capability = 0x32  Neighbor_Report Beacon_Passive Beacon_Active
"""

def test_parse_sta_info_ko_in_field():
    """_summary_
    """
    row = {}
    mac_sta = "80:20:DA:EE:89:A7"
    row = parse_sta_info(SAT_INFO_KO_IN_FILED, mac_sta)
    assert row['BH_STA_INFO_TX_FAILURES_'+mac_sta] == 6
    assert row['BH_STA_INFO_BANDWIDTH_'+mac_sta] == 80
    assert row['BH_STA_INFO_UPTIME_'+mac_sta] == 339317
    assert row['BH_STA_INFO_DECRYPT_FAILURE_'+mac_sta] == 0

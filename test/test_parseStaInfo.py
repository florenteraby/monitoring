import pytest
from monitor import parse_sta_info




STA_INFO = """[VER 8] STA 10:D7:B0:1A:96:6F:
\t chanspec 116/80 (0xe07a)
\t aid:13
\t rateset [ 6 9 12 18 24 36 48 54 ]
\t idle 0 seconds
\t in network 13416 seconds 
\t state: AUTHENTICATED ASSOCIATED AUTHORIZED
\t connection: SECURED
\t auth: WPA2-PSK
\t crypto: AES_CCM
\t flags 0x351e03b: BRCM WME N_CAP VHT_CAP HE_CAP AMPDU AMSDU DWDS_CAP DWDS_ACTIVE
\t HT caps 0x1ef: LDPC 40MHz SGI20 SGI40 STBC-Tx STBC-Rx
\t VHT caps 0xfb: LDPC SGI80 STBC-Tx STBC-Rx SU-BFR SU-BFE MU-BFR
\t HE caps 0x6689: LDPC HE-HTC
\t OMI 0x00f3: 80Mhz rx=4ss tx=4ss UL_MU_DISABLE 
\t TWT info 0x1: CAPABLE
\t tx total pkts: 427850
\t tx total bytes: 145704772
\t tx ucast pkts: 367774
\t tx ucast bytes: 139126948
\t tx mcast/bcast pkts: 60076
\t tx mcast/bcast bytes: 6577824
\t tx failures: 11
\t rx data pkts: 265829
\t rx data bytes: 118666736
\t rx data dur: 0
\t rx ucast pkts: 252389
\t rx ucast bytes: 116006201
\t rx mcast/bcast pkts: 13440
\t rx mcast/bcast bytes: 2660535
\t rate of last tx pkt: 1814790 kbps - 1088880 kbps
\t rate of last rx pkt: 1801470 kbps
\t rx decrypt succeeds: 265824
\t rx decrypt failures: 0
\t tx data pkts retried: 2
\t per antenna rssi of last rx data frame: -31 -32 -32 -32
\t per antenna average rssi of rx data frames: -30 -32 -31 -33
\t per antenna noise floor: -93 -93 -90 -93
\t tx total pkts sent: 367774
\t tx pkts retries: 42782
\t tx pkts retry exhausted: 0
\t tx FW total pkts sent: 19
\t tx FW pkts retries: 1
\t tx FW pkts retry exhausted: 0
\t rx total pkts retried: 4566
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
\t chanspec 116/80 (0xe07a)
\t aid:13
\t rateset [ 6 9 12 18 24 36 48 54 ]
\t idle 0 seconds
\t in network 13416 seconds
\t state: AUTHENTICATED ASSOCIATED AUTHORIZED
\t connection: SECURED
\t auth: WPA2-PSK
\t crypto: AES_CCM
\t flags 0x351e03b: BRCM WME N_CAP VHT_CAP HE_CAP AMPDU AMSDU DWDS_CAP DWDS_ACTIVE
\t HT caps 0x1ef: LDPC 40MHz SGI20 SGI40 STBC-Tx STBC-Rx
\t VHT caps 0xfb: LDPC SGI80 STBC-Tx STBC-Rx SU-BFR SU-BFE MU-BFR
\t HE caps 0x6689: LDPC HE-HTC
\t OMI 0x00f3: 80Mhz rx=4ss tx=4ss UL_MU_DISABLE 
\t TWT info 0x1: CAPABLE
\t tx total pkts: 427850
\t tx total bytes: 145704772
\t tx ucast pkts: 367774
\t tx ucast bytes: 139126948
\t tx mcast/bcast pkts: 60076
\t tx mcast/bcast bytes: 6577824
\t tx failures: 11
\t rx data pkts: 265829
\t rx data bytes: 118666736
\t rx data dur: 0
\t rx ucast pkts: 252389
\t rx ucast bytes: 116006201
\t rx mcast/bcast pkts: 13440
\t rx mcast/bcast bytes: 2660535
\t rate of last tx pkt: 1814790 kbps - 1088880 kbps
\t rate of last rx pkt: 1801470 kbps
\t rx decrypt succeeds: 265824
\t rx decrypt failures: 0
\t tx data pkts retried: 2
\t per antenna rssi of last rx data frame: -31 -32 -32 -32
\t per antenna average rssi of rx data frames: -30 -32 -31 -33
\t per antenna noise floor: -93 -93 -90 -93
\t tx total pkts sent: 367774
\t tx pkts retries: 42782
\t tx pkts retry exhausted: 0
\t tx FW total pkts sent: 19
\t tx FW pkts retries: 1
\t tx FW pkts retry exhausted: 0
\t rx total pkts retried: 4566
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
\t chanspec 116/80 (0xe07a)
\t aid:13
\t rateset [ 6 9 12 18 24 36 48 54 ]
\t idle 0 seconds
\t in network 13416333333 seconds
\t : AUTHENTICATED ASSOCIATED AUTHORIZED
\t ction: SECURED
\t WPA2-PSK
\t crypto: AES_CCM
\t flags 0x351e03b: BRCM WME N_CAP VHT_CAP HE_CAP AMPDU AMSDU DWDS_CAP DWDS_ACTIVE
\t HT caps 0x1ef: LDPC 40MHz SGI20 SGI40 STBC-Tx STBC-Rx
\t VHT caps 0xfb: LDPC SGI80 STBC-Tx STBC-Rx SU-BFR SU-BFE MU-BFR
\t HE caps 0x6689: LDPC HE-HTC
\t OMI 0x00f3: 80Mhz rx=4ss tx=4ss UL_MU_DISABLE 
\t TWT info 0x1: CAPABLE
\t tx total pkts: 427850
\t tx total bytes: 145704772
\t tx ucast pkts: 367774
\t tx ucast bytes: 139126948
\t tx mcast/bcast pkts: 60076
\t tx mcast/bcast bytes: 6577824
\t tx failures: 11
\t rx data pkts: 265829
\t rx data bytes: 118666736
\t rx data dur: 0
\t rx ucast pkts: 252389
\t rx ucast bytes: 116006201
\t rx mcast/bcast pkts: 13440
\t rx mcast/bcast bytes: 2660535
\t rate of last tx pkt: 1814790 kbps - 1088880 kbps
\t rate of last rx pkt: 1801470 kbps
\t rx decrypt succeeds: 265824
\t rx decrypt failures: 0
\t tx data pkts retried: 2
\t per antenna rssi of last rx data frame: -31 -32 -32 -32
\t per antenna average rssi of rx data frames: -30 -32 -31 -33
\t per antenna noise floor: -93 -93 -90 -93
\t tx total pkts sent: 367774
\t tx pkts retries: 42782
\t tx pkts retry exhausted: 0
\t tx FW total pkts sent: 19
\t tx FW pkts retries: 1
\t tx FW pkts retry exhausted: 0
\t rx total pkts retried: 4566
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


STA_INFO_KO_IN_FIELD = """[VER 8] STA 80:20:DA:EE:89:A7:
\t chanspec 136/80 (0xe18a)
\t aid:13 
\t rateset [ 6 9 12 18 24 36 48 54 ]
\t idle 0 seconds
\t in network 339317 seconds
\t state: AUTHENTICATED ASSOCIATED AUTHORIZED
\t connection: SECURED
\t auth: WPA2-PSK
\t crypto: AES_CCM
\t flags 0x351e03b: BRCM WME N_CAP VHT_CAP HE_CAP AMPDU AMSDU DWDS_CAP DWDS_ACTIVE
\t HT caps 0x1ef: LDPC 40MHz SGI20 SGI40 STBC-Tx STBC-Rx
\t VHT caps 0xfb: LDPC SGI80 STBC-Tx STBC-Rx SU-BFR SU-BFE MU-BFR
\t HE caps 0x6689: LDPC HE-HTC
\t OMI 0x00f3: 80Mhz rx=4ss tx=4ss UL_MU_DISABLE 
\t TWT info 0x1: CAPABLE
\t tx total pkts: 37389133
\t tx total bytes: 25822979079
\t tx ucast pkts: 34956578
\t tx ucast bytes: 25527817099
\t tx mcast/bcast pkts: 2432555
\t tx mcast/bcast bytes: 295161980
\t tx failures: 6
\t rx data pkts: 26404505
\t rx data bytes: 11580105720
\t rx data dur: 0
\t rx ucast pkts: 25558142
\t rx ucast bytes: 11396502304
\t rx mcast/bcast pkts: 846363
\t rx mcast/bcast bytes: 183603416
\t rate of last tx pkt: 1152940 kbps - 288230 kbps
\t rate of last rx pkt: 864700 kbps
\t rx decrypt succeeds: 26404403
\t rx decrypt failures: 0
\t tx data pkts retried: 3
\t per antenna rssi of last rx data frame: -67 -63 -67 -64
\t per antenna average rssi of rx data frames: -67 -63 -67 -64
\t per antenna noise floor: -91 -92 -91 -91
\t tx total pkts sent: 34956571
\t tx pkts retries: 4086027
\t tx pkts retry exhausted: 6
\t tx FW total pkts sent: 18
\t tx FW pkts retries: 2
\t tx FW pkts retry exhausted: 0
\t rx total pkts retried: 1830689
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
    row = parse_sta_info(STA_INFO_KO_IN_FIELD, mac_sta)
    assert row['BH_STA_INFO_TX_FAILURES_'+mac_sta] == 6
    assert row['BH_STA_INFO_BANDWIDTH_'+mac_sta] == 80
    assert row['BH_STA_INFO_UPTIME_'+mac_sta] == 339317
    assert row['BH_STA_INFO_DECRYPT_FAILURE_'+mac_sta] == 0

STA_INFO_CHANSPEC_1L = """[VER 8] STA B0:4A:39:4A:7E:A6:
\t chanspec 1l (0x1803)
\t aid:24 
\t rateset [ 1 2 5.5 6 9 11 12 18 24 36 48 54 ]
\t idle 1 seconds
\t in network 3949 seconds
\t state: AUTHENTICATED ASSOCIATED AUTHORIZED
\t connection: SECURED
\t auth: WPA2-PSK
\t crypto: AES_CCM
\t flags 0x1e03a: WME N_CAP AMPDU AMSDU
\t HT caps 0x16e: 40MHz SGI20 SGI40 STBC-Rx
\t tx total pkts: 741267
\t tx total bytes: 250576800
\t tx ucast pkts: 1514
\t tx ucast bytes: 127262
\t tx mcast/bcast pkts: 739753
\t tx mcast/bcast bytes: 250449538
\t tx failures: 14
\t rx data pkts: 1221
\t rx data bytes: 202480
\t rx data dur: 0
\t rx ucast pkts: 403
\t rx ucast bytes: 58953
\t rx mcast/bcast pkts: 818
\t rx mcast/bcast bytes: 143527
\t rate of last tx pkt: 5500 kbps - 1000 kbps
\t rate of last rx pkt: 1000 kbps
\t rx decrypt succeeds: 1132
\t rx decrypt failures: 0
\t tx data pkts retried: 366
\t per antenna rssi of last rx data frame: -86 -87 0 0
\t per antenna average rssi of rx data frames: -86 -88 0 0
\t per antenna noise floor: -87 -87 0 0
\t tx total pkts sent: 1597
\t tx pkts retries: 1033
\t tx pkts retry exhausted: 14
\t tx FW total pkts sent: 0
\t tx FW pkts retries: 0
\t tx FW pkts retry exhausted: 0
\t rx total pkts retried: 327
MCS SET : [ 0 1 2 3 4 5 6 7 ]
smoothed rssi: -86
tx nrate
legacy rate 5.5 Mbps stf mode 0 auto
rx nrate
legacy rate 1 Mbps stf mode 0 auto
wnm
0x0:
VENDOR OUI VALUE[0] 00:50:F2 
link bandwidth = 40 MHZ 
RRM capability = 0x0 
Frequency Bands Supported: 2.4G 
"""
def test_sta_info_chanspec_1l():
    """_summary_
    """
    row = {}
    mac_sta = "B0:4A:39:4A:7E:A6"
    row = parse_sta_info(STA_INFO_CHANSPEC_1L, mac_sta)
    assert row['BH_STA_INFO_TX_FAILURES_'+mac_sta] == 14
    assert row['BH_STA_INFO_BANDWIDTH_'+mac_sta] == 40
    assert row['BH_STA_INFO_UPTIME_'+mac_sta] == 3949
    assert row['BH_STA_INFO_DECRYPT_FAILURE_'+mac_sta] == 0

#!/usr/bin/python
"""_summary_
"""


import pytest
import device_monitor

SAT_INFO_1 = """[VER 8] STA 34:53:D2:FC:E5:12:
	 chanspec 56/160 (0xed32)
	 aid:16 
	 rateset [ 6 9 12 18 24 36 48 54 ]
	 idle 0 seconds
	 in network 601993 seconds
	 state: AUTHENTICATED ASSOCIATED AUTHORIZED
	 connection: SECURED
	 auth: WPA2-PSK
	 crypto: AES_CCM
	 flags 0x7d1e03b: BRCM WME N_CAP VHT_CAP HE_CAP AMPDU AMSDU GBL_RCLASS DWDS_CAP DWDS_ACTIVE MAP
	 HT caps 0x1ef: LDPC 40MHz SGI20 SGI40 STBC-Tx STBC-Rx
	 VHT caps 0xff: LDPC SGI80 SGI160 STBC-Tx STBC-Rx SU-BFR SU-BFE MU-BFR
	 HE caps 0x6639: LDPC HE-HTC SU-BFR SU&MU-BFE
	 OMI 0x02fb: 160Mhz rx=4ss tx=4ss ER_SU_DISABLE UL_MU_DISABLE 
	 tx total pkts: 6982449
	 tx total bytes: 4331833014
	 tx ucast pkts: 4663215
	 tx ucast bytes: 3559450749
	 tx mcast/bcast pkts: 2319234
	 tx mcast/bcast bytes: 772382265
	 tx failures: 53
	 rx data pkts: 3207364
	 rx data bytes: 813311954
	 rx data dur: 0
	 rx ucast pkts: 3192332
	 rx ucast bytes: 811022794
	 rx mcast/bcast pkts: 15032
	 rx mcast/bcast bytes: 2289160
	 rate of last tx pkt: 2882350 kbps - 1633330 kbps
	 rate of last rx pkt: 2882350 kbps
	 rx decrypt succeeds: 3188048
	 rx decrypt failures: 0
	 tx data pkts retried: 8
	 per antenna rssi of last rx data frame: -52 -54 -46 -53
	 per antenna average rssi of rx data frames: -51 -53 -46 -53
	 per antenna noise floor: -90 -89 -88 -91
	 tx total pkts sent: 4662617
	 tx pkts retries: 1839980
	 tx pkts retry exhausted: 53
	 tx FW total pkts sent: 0
	 tx FW pkts retries: 0
	 tx FW pkts retry exhausted: 0
	 rx total pkts retried: 227777
MCS SET : [ 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 ]
VHT SET : 0x1 1x1 2x1 3x1 4x1 5x1 6x1 7x1 8x1 9x1 
        : 0x2 1x2 2x2 3x2 4x2 5x2 6x2 7x2 8x2 9x2 
        : 0x3 1x3 2x3 3x3 4x3 5x3 6x3 7x3 8x3 9x3 
        : 0x4 1x4 2x4 3x4 4x4 5x4 6x4 7x4 8x4 9x4 
HE SET  :
	    20/40/80 MHz:
		NSS1 Tx: 0-11        Rx: 0-11
		NSS2 Tx: 0-11        Rx: 0-11
		NSS3 Tx: 0-11        Rx: 0-11
		NSS4 Tx: 0-11        Rx: 0-11
	    160 MHz:
		NSS1 Tx: 0-11        Rx: 0-11
		NSS2 Tx: 0-11        Rx: 0-11
		NSS3 Tx: 0-11        Rx: 0-11
		NSS4 Tx: 0-11        Rx: 0-11
smoothed rssi: -46
tx nrate
he mcs 9 Nss 3 Tx Exp 1 bw160 ldpc 2xLTF GI 0.8us auto
rx nrate
he mcs 9 Nss 3 Tx Exp 0 bw160 ldpc 2xLTF GI 0.8us auto
wnm
0x1:  BSS-Transition
VENDOR OUI VALUE[0] 00:90:4C 
VENDOR OUI VALUE[1] 00:10:18 
VENDOR OUI VALUE[2] 00:50:F2 
VENDOR OUI VALUE[3] 50:6F:9A 
link bandwidth = 160 MHZ 
RRM capability = 0x32  Neighbor_Report Beacon_Passive Beacon_Active
Frequency Bands Supported: 5G 
"""

def test_parse_station_stats():
    """Test if bandwidth and CHannel are well detected
    """
    station_list = {}
    station_list["34:53:D2:FC:E5:12"] = device_monitor.station_stats(SAT_INFO_1)
    assert station_list["34:53:D2:FC:E5:12"]["chanspec_chan"] == 56
    assert station_list["34:53:D2:FC:E5:12"]["chanspec_bw"] == 160
    assert station_list["34:53:D2:FC:E5:12"]["tx_total_pkts"] == 6982449
    assert station_list["34:53:D2:FC:E5:12"]["tx_mcast/bcast_bytes"] == 772382265
    assert station_list["34:53:D2:FC:E5:12"]["rx_total_pkts_retried"] == 227777
    assert station_list["34:53:D2:FC:E5:12"]["rx_data_bytes"] == 813311954
    assert station_list["34:53:D2:FC:E5:12"]["smoothed_rssi"] == "-46"

def test_parse_station_mcs_nss():
    """Test if bandwidth and CHannel are well detected
    """
    station_list = {}
    station_list["34:53:D2:FC:E5:12"] = device_monitor.station_stats(SAT_INFO_1)
    assert station_list["34:53:D2:FC:E5:12"]["tx_mcs"] == 9
    assert station_list["34:53:D2:FC:E5:12"]["rx_mcs"] == 9
    assert station_list["34:53:D2:FC:E5:12"]["tx_nss"] == 3
    assert station_list["34:53:D2:FC:E5:12"]["rx_nss"] == 3

SAT_INFO_2 = """[VER 8] STA 7E:BA:8E:9E:62:06:
	 chanspec 56/80 (0xe13a)
	 aid:25 
	 rateset [ 6 9 12 18 24 36 48 54 ]
	 idle 0 seconds
	 in network 88767 seconds
	 state: AUTHENTICATED ASSOCIATED AUTHORIZED
	 connection: SECURED
	 auth: WPA2-PSK
	 crypto: AES_CCM
	 flags 0x91e13a: WME PS N_CAP VHT_CAP AMPDU AMSDU GBL_RCLASS
	 HT caps 0x117e: 40MHz GF SGI20 SGI40 STBC-Rx
	 VHT caps 0x152: SGI80 STBC-Rx SU-BFE MU-BFE
	 tx total pkts: 2470967
	 tx total bytes: 1103010483
	 tx ucast pkts: 143357
	 tx ucast bytes: 328243799
	 tx mcast/bcast pkts: 2327610
	 tx mcast/bcast bytes: 774766684
	 tx failures: 0
	 rx data pkts: 160546
	 rx data bytes: 25842845
	 rx data dur: 0
	 rx ucast pkts: 160523
	 rx ucast bytes: 25839794
	 rx mcast/bcast pkts: 23
	 rx mcast/bcast bytes: 3051
	 rate of last tx pkt: 433333 kbps - 260000 kbps
	 rate of last rx pkt: 6000 kbps
	 rx decrypt succeeds: 91517
	 rx decrypt failures: 0
	 tx data pkts retried: 0
	 per antenna rssi of last rx data frame: -32 -30 -41 -27
	 per antenna average rssi of rx data frames: -32 -30 -42 -27
	 per antenna noise floor: -89 -88 -88 -89
	 tx total pkts sent: 145580
	 tx pkts retries: 426
	 tx pkts retry exhausted: 0
	 tx FW total pkts sent: 0
	 tx FW pkts retries: 0
	 tx FW pkts retry exhausted: 0
	 rx total pkts retried: 608
MCS SET : [ 0 1 2 3 4 5 6 7 ]
VHT SET : 0x1 1x1 2x1 3x1 4x1 5x1 6x1 7x1 8x1 9x1 
smoothed rssi: -27
tx nrate
vht mcs 9 Nss 1 Tx Exp 3 bw80 sgi auto
rx nrate
legacy rate 6 Mbps stf mode 0 auto
wnm
0x21:  BSS-Transition  WNM-Sleep-Mode
VENDOR OUI VALUE[0] 00:00:F0 
VENDOR OUI VALUE[1] 00:50:F2 
VENDOR OUI VALUE[2] 00:0C:E7 
link bandwidth = 80 MHZ 
RRM capability = 0x2007b  Link_Measurement Neighbor_Report Repeated_Measurement Beacon_Passive Beacon_Active Beacon_Table RM_MIB
Frequency Bands Supported: 2.4G 5G 
"""
def test_parse_station_mcs_nss_legacy():
    """Test if bandwidth and CHannel are well detected
    """
    list_of_station = []
    station_list = {}
    station_list['MAC'] = "7E:BA:8E:9E:62:06"
    station_list['STATS'] = device_monitor.station_stats(SAT_INFO_2)
    list_of_station.append(station_list)
    station_list['MAC'] = "7E:BA:8E:9E:62:07"
    station_list['STATS'] = device_monitor.station_stats(SAT_INFO_1)
    list_of_station.append(station_list)
    stats = list_of_station[0].get("STATS")
    assert stats["tx_mcs"] == 9

SAT_INFO_3 = """[VER 8] STA 7E:BA:8E:9E:62:06:
	 chanspec 56(0xe13a)
	 aid:25 
	 rateset [ 6 9 12 18 24 36 48 54 ]
	 idle 0 seconds
	 in network 88767 seconds
	 state: AUTHENTICATED ASSOCIATED AUTHORIZED
	 connection: SECURED
	 auth: WPA2-PSK
	 crypto: AES_CCM
	 flags 0x91e13a: WME PS N_CAP VHT_CAP AMPDU AMSDU GBL_RCLASS
	 HT caps 0x117e: 40MHz GF SGI20 SGI40 STBC-Rx
	 VHT caps 0x152: SGI80 STBC-Rx SU-BFE MU-BFE
	 tx total pkts: 2470967
	 tx total bytes: 1103010483
	 tx ucast pkts: 143357
	 tx ucast bytes: 328243799
	 tx mcast/bcast pkts: 2327610
	 tx mcast/bcast bytes: 774766684
	 tx failures: 0
	 rx data pkts: 160546
	 rx data bytes: 25842845
	 rx data dur: 0
	 rx ucast pkts: 160523
	 rx ucast bytes: 25839794
	 rx mcast/bcast pkts: 23
	 rx mcast/bcast bytes: 3051
	 rate of last tx pkt: 433333 kbps - 260000 kbps
	 rate of last rx pkt: 6000 kbps
	 rx decrypt succeeds: 91517
	 rx decrypt failures: 0
	 tx data pkts retried: 0
	 per antenna rssi of last rx data frame: -32 -30 -41 -27
	 per antenna average rssi of rx data frames: -32 -30 -42 -27
	 per antenna noise floor: -89 -88 -88 -89
	 tx total pkts sent: 145580
	 tx pkts retries: 426
	 tx pkts retry exhausted: 0
	 tx FW total pkts sent: 0
	 tx FW pkts retries: 0
	 tx FW pkts retry exhausted: 0
	 rx total pkts retried: 608
MCS SET : [ 0 1 2 3 4 5 6 7 ]
VHT SET : 0x1 1x1 2x1 3x1 4x1 5x1 6x1 7x1 8x1 9x1 
smoothed rssi: -27
tx nrate
vht mcs 9 Nss 1 Tx Exp 3 bw80 sgi auto
rx nrate
legacy rate 6 Mbps stf mode 0 auto
wnm
0x21:  BSS-Transition  WNM-Sleep-Mode
VENDOR OUI VALUE[0] 00:00:F0 
VENDOR OUI VALUE[1] 00:50:F2 
VENDOR OUI VALUE[2] 00:0C:E7 
link bandwidth = 80 MHZ 
RRM capability = 0x2007b  Link_Measurement Neighbor_Report Repeated_Measurement Beacon_Passive Beacon_Active Beacon_Table RM_MIB
Frequency Bands Supported: 2.4G 5G 
"""
def test_parse_station_stats_bw_wrong():
    """Test if bandwidth and CHannel are well detected
    """
    station_list = {}
    station_list["34:53:D2:FC:E5:12"] = device_monitor.station_stats(SAT_INFO_3)
    assert station_list["34:53:D2:FC:E5:12"]["chanspec_chan"] == 56
    assert station_list["34:53:D2:FC:E5:12"]["chanspec_bw"] == 0
    assert station_list["34:53:D2:FC:E5:12"]["tx_total_pkts"] == 2470967


def test_create_device_field_command_error(mocker):
    """test with run command returning an error

    Args:
        mocker (_type_): _description_
    """
    mocker.patch('tools.tools.run_command', return_value=(SAT_INFO_2, False))
    station_list = device_monitor.create_device_fields(ASSOCLIST_ONE_ELEMENT, "wl0.1", "192.168.1.1", "root", "root")
    assert len(station_list) == 0

def test_create_device_field_no_assoc_list(mocker):
    """test with run command returning an error

    Args:
        mocker (_type_): _description_
    """
    mocker.patch('tools.tools.run_command', return_value=(SAT_INFO_2, True))
    station_list = device_monitor.create_device_fields("", "wl0.1", "192.168.1.1", "root", "root")
    assert len(station_list) == 0

ASSOCLIST_ONE_ELEMENT = """assoclist 50:84:92:F1:1A:44
"""

def test_create_device_field(mocker):
    """_summary_

    Args:
        mocker (_type_): _description_
    """
    mocker.patch('tools.tools.run_command', return_value=(SAT_INFO_1, True))
    station_list = device_monitor.create_device_fields(ASSOCLIST_ONE_ELEMENT, "wl0.1", "192.168.1.1", "root", "root")
    assert station_list[0].get('MAC') == "50:84:92:F1:1A:44"
    stats = station_list[0].get('STATS')
    assert stats["tx_mcs"] == 9

ASSOCLIST_TWO_ELEMENT = """assoclist 34:53:D2:FC:E5:12
assoclist 34:53:D2:FC:E8:B2
"""

def test_create_device_field_two_elts(mocker):
    """_summary_

    Args:
        mocker (_type_): _description_
    """
    mocker.patch('tools.tools.run_command', return_value=(SAT_INFO_1, True))
    station_list = []
    station_list = device_monitor.create_device_fields(ASSOCLIST_TWO_ELEMENT, "wl0.1", "192.168.1.1", "root", "root")
    assert station_list[0].get('MAC') == "34:53:D2:FC:E5:12"
    stats = station_list[0].get('STATS')
    assert stats["rx_data_bytes"] == 813311954
    assert station_list[1].get('MAC') == "34:53:D2:FC:E8:B2"
    stats = station_list[1].get('STATS')
    assert stats["rx_ucast_pkts"] == 3192332
    device_influx_db = []
    device_influx_db2 = []
    for station in station_list:
        device_tags = {
            'name' : "TOTO",
            'interface' : "interface",
            'FH_BH':  'FH',
            'MAC' : station.get('MAC')
        }
        device_serie = {
        'time' : 0,
        'measurement' : "DEVICE_AIRTIME",
        'tags' : device_tags,
        'fields' : station.get("STATS")
        }
        device_influx_db.append(device_serie)
    device_influx_db2.extend(device_influx_db)
    for influx in device_influx_db2:
        print (influx.get('tags'))
        print (influx.get('fields'))
        print (influx.keys())
        print (influx.get('fields').keys())

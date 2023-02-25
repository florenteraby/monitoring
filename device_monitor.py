#!/usr/bin/python
# coding: utf-8
"""_summary_

    Returns:
        _type_: _description_
"""

import logging
from tools import tools

device_command_assoclist_list = [
    ["/usr/bin/wlctl -i wl0.1 assoclist", "wl0.1", "FH"],
    ["/usr/bin/wlctl -i wl0.3 assoclist", "wl0.3", "BH"],
    ["/usr/bin/wlctl -i wl1 assoclist", "wl1", "FH"]
]

def station_stats(sta_info_result):
    """pasre the sta info
[VER 8] STA 34:53:D2:FC:E5:12:
	 chanspec 56/160 (0xed32)
	 aid:16 
	 rateset [ 6 9 12 18 24 36 48 54 ]
	 idle 0 seconds
	 in network 601527 seconds
	 state: AUTHENTICATED ASSOCIATED AUTHORIZED
	 connection: SECURED
	 auth: WPA2-PSK
	 crypto: AES_CCM
	 flags 0x7d1e03b: BRCM WME N_CAP VHT_CAP HE_CAP AMPDU AMSDU GBL_RCLASS DWDS_CAP DWDS_ACTIVE MAP
	 HT caps 0x1ef: LDPC 40MHz SGI20 SGI40 STBC-Tx STBC-Rx
	 VHT caps 0xff: LDPC SGI80 SGI160 STBC-Tx STBC-Rx SU-BFR SU-BFE MU-BFR
	 HE caps 0x6639: LDPC HE-HTC SU-BFR SU&MU-BFE
	 OMI 0x02fb: 160Mhz rx=4ss tx=4ss ER_SU_DISABLE UL_MU_DISABLE 
	 tx total pkts: 6975397
	 tx total bytes: 4329613284
	 tx ucast pkts: 4658279
	 tx ucast bytes: 3557871124
	 tx mcast/bcast pkts: 2317118
	 tx mcast/bcast bytes: 771742160
	 tx failures: 53
	 rx data pkts: 3202908
	 rx data bytes: 811967595
	 rx data dur: 0
	 rx ucast pkts: 3188218
	 rx ucast bytes: 809751869
	 rx mcast/bcast pkts: 14690
	 rx mcast/bcast bytes: 2215726
	 rate of last tx pkt: 2722220 kbps - 1633330 kbps
	 rate of last rx pkt: 2882350 kbps
	 rx decrypt succeeds: 3183592
	 rx decrypt failures: 0
	 tx data pkts retried: 8
	 per antenna rssi of last rx data frame: -51 -53 -45 -52
	 per antenna average rssi of rx data frames: -51 -53 -45 -52
	 per antenna noise floor: -90 -89 -88 -91
	 tx total pkts sent: 4657681
	 tx pkts retries: 1839504
	 tx pkts retry exhausted: 53
	 tx FW total pkts sent: 0
	 tx FW pkts retries: 0
	 tx FW pkts retry exhausted: 0
	 rx total pkts retried: 227545
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
smoothed rssi: -45
tx nrate
he mcs 9 Nss 3 Tx Exp 1 bw160 ldpc 2xLTF GI 1.6us auto
rx nrate
he mcs 9 Nss 3 Tx Exp 0 bw160 ldpc 2xLTF GI 0.8us auto
wnm
0x1:  BSS-Transition
VENDOR OUI VALUE[0] 00:90:4C 
VENDOR OUI VALUE[1] 00:10:18 4:53:D2:F
VENDOR OUI VALUE[2] 00:50:F2 
VENDOR OUI VALUE[3] 50:6F:9A 
link bandwidth = 160 MHZ 
RRM capability = 0x32  Neighbor_Report Beacon_Passive Beacon_Active
Frequency Bands Supported: 5G 
    Args:
        sta_info_result (str): see above
    """
    my_station_stats = {}
    tx_nrate = False
    rx_nrate = False

    for sta_info_line in sta_info_result.splitlines():
        if "chanspec" in sta_info_line:
            my_station_stats["chanspec_chan"] = int(sta_info_line.split(" ")[2].split("/")[0])
            my_station_stats["chanspec_bw"] = int(sta_info_line.split(" ")[2].split("/")[1])
        to_find = ["tx total", "tx ucast", "tx mcast/bcast", "tx failures", "rx data pkts", "rx data bytes","rx ucast", "rx mcast/bcast", "rx mcast/bcast", "tx pkts", "rx total"]
        for my_string in to_find:
            if my_string in sta_info_line:
                index_name =sta_info_line.split(":")[0].strip("\t ").replace(" ", "_")
                my_station_stats[index_name] = int(sta_info_line.split(":")[1])
        if "smoothed rssi" in sta_info_line:
            my_station_stats["smoothed_rssi"] = sta_info_line.split(":")[1].strip()
        if tx_nrate is True or rx_nrate is True:
            rate = sta_info_line.split(" ")
            if "legacy" == rate[0]:
                mcs = 0
                nss = 0
            else:
                mcs = int(rate[2])
                nss = int(rate[4])
            if rx_nrate is True:
                my_station_stats["rx_mcs"] = mcs
                my_station_stats["rx_nss"] = nss
                rx_nrate = False
            if tx_nrate is True:
                my_station_stats["tx_mcs"] = mcs
                my_station_stats["tx_nss"] = nss
                tx_nrate = False
        if "tx nrate" in sta_info_line:
            tx_nrate = True
        if "rx nrate" in sta_info_line:
            rx_nrate = True
    return my_station_stats

def create_device_fields(result_to_parse, interface, ip, username, password):
    """Get the result of the assoclist command. the output is the list of station indexed by MAC with all stats available

    Args:
        result_to_parse (str): result of assoclist command, can be empty
        interface (str): WiFI interface to executre commade
        ip (str): ip of the extender
        username (str): username
        password (str): password
    """
    logger = logging.getLogger()
    stations_list = []
    for line in result_to_parse.splitlines():
        station_mac =  line.split(" ")[1]
        sta_info_command = "wlctl -i "+interface+" sta_info "+station_mac
        command_to_execute = tools.prepare_command(sta_info_command, ip, username, password, logger)
        output, success = tools.run_command(command_to_execute, logger)
        if success is True:
            device_stats = {
                'MAC': station_mac,
                'STATS' : station_stats(output)
            }
            stations_list.append(device_stats)
    return stations_list

def create_device_serie(extender, timestamp):
    """_summary_

    Args:
        extender (_type_): _description_

    Returns:
        _type_: _description_
    """
    device_serie_list = []
    logger = logging.getLogger()

    for command, interface, bh_fh in device_command_assoclist_list:
        to_execute = tools.prepare_command(command, extender['ip'], extender['username'], extender['password'], logger)
        output, success = tools.run_command(to_execute, logger)
        if success is True:
            stations = create_device_fields(output, interface, extender['ip'], extender['username'], extender['password'],)
        else:
            stations = []

        for station in stations:

            device_tags = {
                'name' : extender['name'].strip(),
                'interface' : interface,
                'FH_BH' : bh_fh,
                'MAC' : station.get('MAC')
            }
            device_serie = {
                'time' : timestamp,
                'measurement' : "DEVICE_AIRTIME",
                'tags' : device_tags,
                'fields' : station.get("STATS")
            }
            device_serie_list.append(device_serie)
    return device_serie_list

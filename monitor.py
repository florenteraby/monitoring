#!/usr/bin/python
# coding: utf-8

"""_summary_

    Returns:
        _type_: _description_
"""

from sys import version_info

#Local packages

import sys
import getopt
import logging
import csv
import time
import json
import datetime
import os

#from tools.config_file import *
from tools.tools import prepare_command, run_command
from device_monitor import create_device_serie

if version_info[0] >=3:
    import influxdb_client
    from influxdb_client import InfluxDBClient, Point
    from influxdb_client.client.write_api import SYNCHRONOUS
else :
    from influxdb import InfluxDBClient
    print ("%s", version_info)




LOG_FORMAT = "%(levelname)s %(asctime)s %(funcName)s- %(message)s"
DEFAULT_POLLING_FREQUENCY = 600

common_command_list = [
["/usr/bin/xmo-client -p Device/DeviceInfo/RebootCount", "REBOOT"],
["/usr/bin/xmo-client -p Device/DeviceInfo/ExternalFirmwareVersion", "FIRMWARE_VERSION"],
["/usr/bin/xmo-client -p Device/DeviceInfo/ModelNumber", "MODELE_NAME"],
["cat /proc/uptime", "UPTIME"],
["cat /proc/meminfo | grep -iw memfree", "MEMINFO_MEMFREE"],
["cat /proc/meminfo | grep -iw MemAvailable:", "MEMINFO_MEMAVAILABLE"],
["cat /proc/meminfo | grep -iw MemTotal:", "MEMINFO_MEMTOTAL"],
["cat /proc/meminfo | grep -iw buffers", "MEMINFO_BUFFER"],
["cat /proc/meminfo | grep -iw cached", "MEMINFO_CACHED"],
["cat /sys/class/ubi/ubi0*/max_ec", "MAX_EC_UBI0"],
["cat /sys/class/ubi/ubi0*/bad_peb_count", "BAD_PEB_COUNT_UBI0"],
["cat /sys/class/ubi/ubi0*/total_eraseblocks", "TOTAL_ERASE_BLOCKS_UBI0"],
["cat /sys/class/ubi/ubi1*/max_ec", "MAX_EC_UBI1"],
["cat /sys/class/ubi/ubi1*/bad_peb_count", "BAD_PEB_COUNT_UBI1"],
["cat /sys/class/ubi/ubi1*/total_eraseblocks", "TOTAL_ERASE_BLOCKS_UBI1"],
["cat /sys/class/ubi/ubi2*/max_ec", "MAX_EC_UBI2"],
["cat /sys/class/ubi/ubi2*/bad_peb_count", "BAD_PEB_COUNT_UBI2"],
["cat /sys/class/ubi/ubi2*/total_eraseblocks", "TOTAL_ERASE_BLOCKS_UBI2"],
["cat /proc/loadavg", "LOADAVG"],
["vmstat", "VMSTAT"],
["ps", "VMZ_PS"],
["top -bn 1", "TOP"],
# ["ps | grep -w hg6d", "VMZ_HG6D"],
# ["ps | grep -w wshd", "VMZ_WSHD"],
# ["ps | grep -w wstd", "VMZ_WSTPD"],
# ["ps | grep -w dhclient", "VMZ_DHCLIENT"],
# ["ps | grep -w dhcrelay", "VMZ_DHCPRELAY"],
# ["ps | grep -w ismd", "VMZ_ISMD"],
# ["ps | grep -w dnsmasq", "VMZ_DNSMASQ"],
["du -s /tmp", "TMP_FS_SIZE"],
["du -s /opt/conf/", "CONF_FS_SIZE"],
["du -s /opt/data/", "DATA_FS_SIZE"],
["ps | grep hostapd | wc -l", "NB_HOSTAPD"],
["cat /opt/data/dumpcore.history | wc -l", "NB_DUMPCORE"],
["ping -c1 8.8.8.8", "PING_WO_DNS"]
# ["nslookup -debug www.microsoft.com", "DNS_RESOLUTION_MICROSOFT"],
# ["nslookup -debug www.google.com", "DNS_RESOLUTION_GOOGLE"],
]

system_command_list_F398BT = common_command_list + [
["/usr/bin/xmo-client -p Device/Services/BTServices/BTGlobalState/TemperatureMonitoring/Temperature", "TEMPERATURE"],
#TODO Add hg6d, wshd VM SIZE command add data usage file size monitoring

["/usr/bin/xmo-client -p Device/Services/BTServices/BTDevicesMgt/Devices/Device/Active | grep true -c", "NBCONNECTEDCLIENT"],
["/usr/bin/xmo-client -p Device/Services/BTServices/BTDevicesMgt/Devices/Device[ConnectionType=\\'ETH\\']/Active | grep true -c", "NBETHCONNECTEDCLIENT"],
["/usr/bin/xmo-client -p Device/Services/BTServices/BTDevicesMgt/Devices/Device[ConnectionType=\\'WL\\']/Active | grep true -c", "NBWLCONNECTEDCLIENT"],
#TODO Add wshd PID monitoring
["/usr/sbin/wlctl -i wl0 channel", "WIFI_CHANNEL_BH"],
["/usr/sbin/wlctl -i wl0.2 assoclist", "WIFI_BH_ASSOCLIST"],
#F398
["/usr/sbin/wlctl -i wl1 channel", "WIFI_CHANNEL_5G"],
#F398
["/usr/sbin/wlctl -i wl2 channel", "WIFI_CHANNEL_24G"],
["/usr/sbin/wlctl -i wl0 chanim_stats", "WIFI_CHANIM_BH"],
#F398
["/usr/sbin/wlctl -i wl1 chanim_stats", "WIFI_CHANIM_5G"],
#F398
["/usr/sbin/wlctl -i wl2 chanim_stats", "WIFI_CHANIM_24G"],
["/usr/bin/xmo-client -p Device/WiFi/Radios/Radio[1]/Channel", "WIFI_CONFIG_CHANNEL_24G"],
["/usr/bin/xmo-client -p Device/WiFi/Radios/Radio[2]/Channel", "WIFI_CONFIG_CHANNEL_5G"],
["/usr/bin/xmo-client -p Device/WiFi/Radios/Radio[3]/Channel", "WIFI_CONFIG_CHANNEL_BH"],
["/usr/sbin/wlctl -i wl1.1 assoclist > /tmp/assoc | /usr/sbin/wlctl -i wl2 assoclist >> /tmp/assoc | /usr/sbin/wlctl -i wl1 assoclist > /tmp/assoc | /usr/sbin/wlctl -i wl2.1 assoclist >> /tmp/assoc; wc -l /tmp/assoc", "NB_CLIENT_WIFI_CONNECTED"],
["/usr/bin/xmo-client -p Device/Services/BTServices/BTDiscsMgt/Discs/Disc/Topology/BackhaulAccessPoint", "BACKHAUL_AP_ID"],
["/usr/bin/xmo-client -p Device/Services/BTServices/BTDiscsMgt/Discs/Disc/Topology/BackhaulConnexionType", "BACKHAUL_AP_TYPE"],
["/usr/bin/xmo-client -p Device/Services/BTServices/BTDiscsMgt/Discs/Disc/Topology/BackhaulRSSI", "BACKHAUL_AP_RSSI"],
["/usr/bin/xmo-client -p Device/Services/BTServices/BTDevicesMgt/Devices/Device[ConnectionType=\\'WL\\'] | grep -e MACAddress -e RSSI -e Layer1Interface -e Name -e Active -e Connected -e Band", "DEVICE_STATUS"],
["du -s /opt/conf/datausage.db", "DATA_USAGE_FS_SIZE"],
["/usr/sbin/infos-cli -t OSM_MASTER_ELECTION -c all | grep ElecState", "ELEC_STATE"]
]

system_command_list_F266GEN = common_command_list + [
["xmo-client -p Device/DeviceInfo/TemperatureStatus/TemperatureSensors/TemperatureSensor/Value", "TEMPERATURE"],
["ps | grep -w data-collector", "VMZ_DATACOLLECTOR"],
["ps | grep -w halwifi", "VMZ_HALWIFI"],
["/usr/bin/xmo-client -p Device/Services/WSHDServices/WSHDDevicesMgt/Devices/Device/Active | grep true -c", "NBCONNECTEDCLIENT"],
["/usr/bin/xmo-client -p Device/Services/WSHDServices/WSHDDevicesMgt/Devices/Device[ConnectionType=\\'ETH\\']/Active | grep true -c", "NBETHCONNECTEDCLIENT"],
["/usr/bin/xmo-client -p Device/Services/WSHDServices/WSHDDevicesMgt/Devices/Device[ConnectionType=\\'WL\\']/Active | grep true -c", "NBWLCONNECTEDCLIENT"],
#TODO Add wshd PID monitoring
["/usr/sbin/wlctl -i wl0 channel", "WIFI_CHANNEL_5G"],
["/usr/sbin/wlctl -i wl1 channel", "WIFI_CHANNEL_24G"],
["/usr/sbin/wlctl -i wl0 chanim_stats", "WIFI_CHANIM_5G"],
["/usr/sbin/wlctl -i wl1 chanim_stats", "WIFI_CHANIM_24G"],
["/usr/sbin/wlctl -i wl1 assoclist > /tmp/assoc | /usr/sbin/wlctl -i wl0.1 assoclist >> /tmp/assoc ; wc -l /tmp/assoc", "NB_CLIENT_WIFI_CONNECTED"],
["/usr/bin/xmo-client -p Device/Services/WSHDServices/WSHDDiscsMgt/Discs/Disc/Topology/BackhaulAccessPoint", "BACKHAUL_AP_ID"],
["/usr/bin/xmo-client -p Device/Services/WSHDServices/WSHDDiscsMgt/Discs/Disc/Topology/BackhaulConnexionType", "BACKHAUL_AP_TYPE"],
["/usr/bin/xmo-client -p Device/Services/WSHDServices/WSHDDiscsMgt/Discs/Disc/Topology/BackhaulRSSI", "BACKHAUL_AP_RSSI"],
["/usr/bin/xmo-client -p Device/Services/WSHDServices/WSHDDevicesMgt/Devices/Device[ConnectionType=\\'NONE\\'] | grep -e MACAddress -e RSSI -e Layer1Interface -e Name -e Active -e Band", "DEVICE_STATUS"]
]

system_command_list_F266GENEMEXT = common_command_list + [
["xmo-client -p Device/DeviceInfo/TemperatureStatus/TemperatureSensors/TemperatureSensor/Value", "TEMPERATURE"],
["ps | grep -w data-collector", "VMZ_DATACOLLECTOR"],
["ps | grep -w halwifi", "VMZ_HALWIFI"],
#TODO Add wshd PID monitoring
["/usr/sbin/wlctl -i wl0 status", "BACKHAUL_AP_RSSI_GENEMEXT"],
["/usr/sbin/wlctl -i wl0 channel", "WIFI_CHANNEL_5G"],
["/usr/sbin/wlctl -i wl1 channel", "WIFI_CHANNEL_24G"],
["/usr/sbin/wlctl -i wl0 chanim_stats", "WIFI_CHANIM_5G"],
["/usr/sbin/wlctl -i wl1 chanim_stats", "WIFI_CHANIM_24G"],
["/usr/sbin/wlctl -i wl1 assoclist > /tmp/assoc | /usr/sbin/wlctl -i wl0.1 assoclist >> /tmp/assoc ; wc -l /tmp/assoc", "NB_CLIENT_WIFI_CONNECTED"]
]


chanim_info = ["chanspec", "tx", "inbss","obss","nocat","nopkt","doze","txop","goodtx","badtx","glitch","badplcp","knoise","idle","timestamp"]
vmstat_info = ["nb_process_running", "nb_process_sleep", "swap", "free", "buff", "cache", "si", "so", "bi", "bo", "interrupt", "context_switch", "user", "system", "idle","wait"]
loadavg_info = ["1MN", "5MN", "15MN"]

def usage(argv):
    """_summary_

    Args:
        argv (_type_): _description_
    """
    print("Usage ù %s", argv)
    print ("[-h, --help]: \t\tthis Message")
    print ("[-t, --type]: \tSystem type")
    print ("\t\t Supported type :")
    print ("\t\t F398BT --> BT F398")
    print ("\t\t F266GEN --> GENERIC F266")
    print ("[-c, --config]: \tMandatory Config file with the format")
    print ("\t\t\t@IP, ROLE, PLACE, LOGIN, PASSWORD")
    print ("[-f, --frequency]: \tOptional Polling frequency (default:%ds)", DEFAULT_POLLING_FREQUENCY)
    print ("[-d, --destfile]: \tMandatory root name of the CSV destination file")
    print ("[-v, --verbose]: \tOptional set debug level mode")

def parse_wl_status(wl_status_result):
    """Parse the wl -i wl0 command to retubr the backhaul rssi if connected, 0 if not

    Args:
        wl_status_result (str): the result of the command to parse

    Returns:
        int: rssi value, or 0 if not connected
    """
    wl_status_line= wl_status_result.splitlines()
    for line in wl_status_line :
        wl_status_result = line.split(" ")
        wl_status = [elt for elt in wl_status_result if elt.strip()]
        if "Not" in wl_status:
            return "0"
        try:
            rssi_index = wl_status.index("Managed\tRSSI:")
        except ValueError:
            pass
        else:
            return wl_status[rssi_index + 1]
    return "0"

def parse_top(top_cmd, row):
    """parse the top command result to separate each procee and provide at list the cpu load per process


    Args:
        top_cmd (str): result of the command in string
    """
    top_lines = top_cmd.splitlines()
    for line in top_lines:
        top_result = line.split(" ")
        top_line = [elt for elt in top_result if elt.strip()]
        try :
            top_line.index("Mem:")
        except ValueError:
            try :
                top_line.index("CPU:")
            except ValueError:
                try:
                    top_line.index("PID")
                except ValueError:
                    try :
                        top_line.index("Load")
                    except ValueError:
                        if len(top_line) != 0:
                            row["TOP_PROCESS"+"_"+top_line[7]] = int(top_line[6].strip("%"))
            else:
                for i in range (1, len (top_line), 2) :
                    row["TOP_CPU"+"_"+top_line[i+1]] = int(top_line[i].strip("%"))

def parse_election_state(to_parse):
    """_summary_

    Args:
        to_parse (_type_): _description_

    Returns:
        _type_: _description_
    """
    my_liste = to_parse.split(",")
    election_state = my_liste[0].split(" ")[1].strip("<").strip(">")
    return election_state

def get_vmz(ps_result, logger):
    """_summary_

    Args:
        ps_result (_type_): _description_
        logger (_type_): _description_

    Returns:
        _type_: _description_
    """
    index_status = 0
    try :
        index_status = ps_result.split(" ").index("R")
        logger.debug("-> Detect process in R")
    except ValueError:
        try :
            index_status = ps_result.split(" ").index("S")
            logger.debug("{} -> Detect process in S")
        except ValueError:
            try :
                index_status = ps_result.split(" ").index("D")
                logger.debug("{} -> Detect process in D")
            except ValueError:
                logger.error("Cannot find index %s", ps_result)
                vmz_size = -1
    finally:
        vmz_size = ps_result.split(" ")[index_status - 1]
        if "m" in vmz_size:
            vmz_size = vmz_size.replace("m", "000000")
        logger.debug("VMZ is %d", int(vmz_size))

    return int(vmz_size)


def parse_process_vmz(output, row, logger):
    """_summary_

    Args:
        output (_type_): _description_
        row (_type_): _description_
        logger (_type_): _description_
    """
    ps_list = output.split("\n")
    for ps_result in ps_list:
        if "hg6d" in ps_result:
            row["VMZ_HG6D"] = get_vmz(ps_result, logger)
        if "wshd" in ps_result:
            row["VMZ_WSHD"] = get_vmz(ps_result, logger)
        if "wstd" in ps_result:
            row["VMZ_WSTD"] = get_vmz(ps_result, logger)
        if "dhclient" in ps_result:
            row["VMZ_DHCLIENT"] = get_vmz(ps_result, logger)
        if "dhcrelay" in ps_result:
            row["VMZ_DHRELAY"] = get_vmz(ps_result, logger)
        if "ismd" in ps_result:
            row["VMZ_ISMD"] = get_vmz(ps_result, logger)
        if "dnsmasq" in ps_result:
            row["VMZ_DNSMASQ"] = get_vmz(ps_result, logger)
        if "hal_wifi" in ps_result:
            row["VMZ_HALWIFI"] = get_vmz(ps_result, logger)

# """ ''' deviceParseResult example of result
# We can see on F@ST266 the foloowing result
#     MACAddress : '74:e5:f9:f1:bc:6f'
#     Name : 'rmm-p2100409pl'
#     Active : 'true'
#     RSSI : '-65'
#     Layer1Interface : 'Device/WiFi/Radios/Radio[RADIO5G]'
#     MACAddress : 'b8:27:eb:38:b3:93'
#     Name : 'B8:27:EB:38:B3:93'
#     Active : 'true'
#     RSSI : '0'
#     Layer1Interface : 'Device/WiFi/Radios/Radio[RADIO2G4]'
#     MACAddress : 'B8:27:EB:54:83:86'
#     Name : 'B8:27:EB:54:83:86'
#     Active : 'false'
#     RSSI : '0'
#     Layer1Interface : 'Device/Ethernet/Interfaces/Interface[PHY2]'
#     MACAddress : '58:E2:8F:19:CD:36'
#     Name : 'iPhonedeFlorent'
#     Active : 'false'
#     RSSI : '-66'
#     Layer1Interface : 'Device/WiFi/Radios/Radio[RADIO5G]'
#     MACAddress : 'b0:0c:d1:5a:6f:6c'
#     Name : 'CSM-9015427'
#     Active : 'true'
#     RSSI : '0'
#     Layer1Interface : ''

# On WHW2 here is the result :
#     MACAddress : 'D8:F2:CA:89:CC:F4'
#     Name : 'RMM-P2100723PW'
#     Active : 'false'
#     ConnectedDisc : ''
#     RSSI : '-64'
#     MACAddress : '5C:AA:FD:F0:94:9A'
#     Name : 'SonosZP'
#     Active : 'true'
#     ConnectedDisc : 'Device/Services/BTServices/BTDiscsMgt/Discs/Disc[@uid='3']'
#     RSSI : '-48'
#     MACAddress : '78:28:CA:2A:A3:AA'
#     Name : 'SonosZP'
#     Active : 'true'
#     ConnectedDisc : 'Device/Services/BTServices/BTDiscsMgt/Discs/Disc[@uid='1']'
#     RSSI : '-70'
#     MACAddress : 'B8:27:EB:6D:80:77'
#     Name : 'pi-FRy'
#     Active : 'true'
#     ConnectedDisc : 'Device/Services/BTServices/BTDiscsMgt/Discs/Disc[@uid='1']'
#     RSSI : '0'
#     MACAddress : 'A4:6C:F1:0D:AD:9E'
#     Name : 'Galaxy-A5-2017'
#     Active : 'true'
#     ConnectedDisc : 'Device/Services/BTServices/BTDiscsMgt/Discs/Disc[@uid='3']'
#     RSSI : '-75'
#     MACAddress : '9C:2E:A1:F9:26:2B'
#     Name : 'Redmi5Plus-theomag'
#     Active : 'true'
#     ConnectedDisc : 'Device/Services/BTServices/BTDiscsMgt/Discs/Disc[@uid='2']'
#     RSSI : '-52'

# every sample has to be sent to the server
# tag (MACADRESS)/tag (DeviceName)
# field (active)
# field (RSSI)
# field (ConnectedDisc(only the UID of the DISC)
# '''
def device_parse_result(to_parse, extender_name, fw_version, model_name, client):
    """_summary_

    Args:
        to_parse (_type_): _description_
        extender_name (_type_): _description_
        fw_version (_type_): _description_
        model_name (_type_): _description_
        client (_type_): _description_
    """
    timestamp = datetime.datetime.utcnow().isoformat()

    if len(to_parse) == 0:
        return
    else:
        serie = []
        fields = {}
        while True:
            try :
                elt = to_parse.pop(0)
            except IndexError :
                break

            if "MACAddress" in elt:
                mac_address = (elt.split("   MACAddress : ")[1].replace("'", ""))
                fields['MACAddress'] = mac_address
            if "Name" in elt:
                fields['Name'] = elt.split("   Name : ")[1].replace("'", "")
            if "Active" in elt:
                fields['Active'] = elt.split("   Active : ")[1].replace("'", "")
            if "ConnectedDisc" in elt:
                if len(elt.split("   ConnectedDisc : ")[1].replace("'", "").split("=")) == 1:
                    fields['ConnectedDisc'] = "NA"
                else :
                    fields['ConnectedDisc'] = elt.split("   ConnectedDisc : ")[1].replace("'", "").split("=")[1].strip("]")
            if "RSSI" in elt:
                fields['RSSI'] = elt.split("   RSSI : ")[1].replace("'", "")
            if "Band" in elt:
                to_send_to_influx_db = {}
                device_tags = {}
                fields['Band'] = elt.split("   Band : ")[1].replace("'", "")

                device_tags = {
                'MACAddress'    : mac_address,
                'DeviceName'    : fields['Name'],
                'name'          : extender_name,
                'fw_version'    : fw_version,
                'model_name'    : model_name
                }

                to_send_to_influx_db = {
                'time' : timestamp,
                'measurement' : "DEVICE",
                'tags' : device_tags,
                'fields' : fields,
                }
                serie.append(to_send_to_influx_db)

                # for myInflux in serie:
                #     print ("Envoie de la serie {}".format(myInflux))
                client.write_points(serie, time_precision='s',database="myDBExample")
                fields = {}
    return
# assoclist 10:D7:B0:1A:96:6F
# assoclist 10:D7:B0:1A:96:7B
def parse_bh_assoclist(to_parse, row, command_type, success_command):
    """_summary_

    Args:
        to_parse (_type_): _description_
        row (_type_): _description_
        command_type (_type_): _description_
        success_command (_type_): _description_

    Returns:
        _type_: _description_
    """
    if success_command is True:
        if len(to_parse) == 0:
            row[command_type] = 0
            return ""
        else:
            my_list = to_parse.split("\n")
            del my_list[-1]
            row[command_type] = len(my_list)
            return my_list
    return ""

def chanim_add_value(to_parse, row, command_type, success_command):
    """_summary_

    Args:
        to_parse (_type_): _description_
        row (_type_): _description_
        command_type (_type_): _description_
        success_command (_type_): _description_
    """
    if success_command is True:
        chanim_answer = to_parse.split("\n")[2].split("\t")
        i = 0
        if len(chanim_answer) < 1:
            i = 0
            for chanim in chanim_info:
                row[command_type + "-" + chanim] = -1
                i = i + 1
            return
        for chanim in chanim_info:
            try :
                chanim_answer[i].isdigit()
            except IndexError:
                print ("Index Error %d %s", i, chanim_answer)
            else:
                if chanim_answer[i].isdigit():
                    row[command_type + "-" + chanim] = int(chanim_answer[i])
                elif chanim_answer[i].isalnum():
                    row[command_type + "-" + chanim] = 0 #chanim_answer[i]
                i = i + 1
    else:
        i = 0
        for chanim in chanim_info:
            row[command_type + "-" + chanim] = -1
            i = i + 1

def vm_stat_add_value(to_parse, row, command_type, success_command):
    """_summary_

    Args:
        to_parse (_type_): _description_
        row (_type_): _description_
        command_type (_type_): _description_
        success_command (_type_): _description_
    """
    vmstat_list = []
    if success_command is True:
        vmstat_list = filter(lambda x: x != "", to_parse.split("\n")[2].split(" "))
        i = 0
        for vmstats in vmstat_info:
            row[command_type + "-" + vmstats] = int(next(vmstat_list))
            i = i + 1
    else:
        i = 0
        for vmstat in vmstat_info:
            row[command_type + "-" + vmstat] = -1
            i = i + 1

def loadavg_add_value(to_parse, row, command_type, success_command):
    """_summary_

    Args:
        to_parse (_type_): _description_

    Returns:
        _type_: _description_
    """
    if success_command is True:
        i = 0
        for loadavg in loadavg_info:
            row[command_type + "-" + loadavg] = float(to_parse.split(" ")[i])
            i = i + 1
    else:
        i = 0
        for loadavg in loadavg_info:
            row[command_type + "-" + loadavg] = float("0")
            i = i + 1

#""" PING 8.8.8.8 (8.8.8.8): 56 data bytes
#64 bytes from 8.8.8.8: seq=0 ttl=115 time=13.199 ms
#
#--- 8.8.8.8 ping statistics ---
#1 packets transmitted, 1 packets received, 0% packet loss
#round-trip min/avg/max = 13.199/13.199/13.199 ms
#
#root@ftr-3140:~# ping -c1 255.255.255.255
#PING 255.255.255.255 (255.255.255.255): 56 data bytes
#
#--- 255.255.255.255 ping statistics ---
#1 packets transmitted, 0 packets received, 100% packet loss
#"""
def parse_ping_wodns(to_parse):
    """_summary_

    Args:
        to_parse (_type_): _description_

    Returns:
        _type_: _description_
    """
    round_trip = -1.0
    ping_parsed = to_parse.split("\n")
    for elt in ping_parsed:
        if "round-trip" in elt:
            round_trip = elt.split("=")[1].split("/")[0].strip(" ")

    return float(round_trip)

def parse_dns_resolution(to_parse):
    """_summary_

    Args:
        to_parse (_type_): _description_

    Returns:
        _type_: _description_
    """
    query_ipv4 = -1
    qurey_ipv6 = -1

    return (query_ipv4, qurey_ipv6)

def update_row(to_parse, success_command, command_type, logger):
    """_summary_

    Args:
        to_parse (_type_): _description_
        success_command (_type_): _description_
        command_type (_type_): _description_
        logger (_type_): _description_

    Returns:
        _type_: _description_
    """
    row = {}
    if success_command is  False:
        if "WIFI_CHANIM" in command_type:
            chanim_add_value(to_parse, row, command_type, success_command)
        elif "VMSTAT" in command_type:
            vm_stat_add_value(to_parse, row, command_type, success_command)
        elif "LOADAVG" in command_type:
            loadavg_add_value(to_parse, row, command_type, success_command)
        elif "BACKHAUL_AP_ID" in command_type :
            row[command_type] = "NA"
        elif "BACKHAUL_AP_TYPE" in command_type :
            row[command_type] = "NA"
        elif "BACKHAUL_AP_RSSI_GENEMEXT" in command_type:
            row[command_type] = "0"
        elif "BACKHAUL_AP_RSSI" in command_type :
            row[command_type] = "0"
        elif "FIRMWARE_VERSION" in command_type :
            row[command_type] = "NA"
        elif "DEVICE_STATUS" in command_type:
            row[command_type] = []
        elif "MEMINFO" in command_type:
            row[command_type] = float("0")
        elif "MODELE_NAME" in command_type:
            row[command_type] = "NA"
        elif "UPTIME" in command_type:
            row[command_type] = float("0")
        elif "NB_CLIENT_WIFI_CONNECTED" in command_type:
            row[command_type] = "0"
        elif "ELEC_STATE" in command_type:
            row[command_type] = "UNKNOWN"
        elif "PING_WO_DNS" in command_type:
            row[command_type] = -1.0
        else:
            row[command_type] = -1
            logger.debug("Command %d failed", row)
    else :
        if command_type == "UPTIME":
            row[command_type] = float(to_parse.split(" ")[0])
        elif "ELEC_STATE" in command_type:
            row[command_type] = parse_election_state(to_parse)
        elif "MEMINFO" in command_type :
            if to_parse.split(":")[1].strip().split(" ")[0].strip().isalnum() is True:
                row[command_type] = float(to_parse.split(":")[1].strip().split(" ")[0].strip())
            else :
                logger.error("Command type return non digit %s %s", to_parse.split(":")[1].strip().split(" ")[0].strip(),to_parse)
                row[command_type] = -1
        elif "MAX_EC" in command_type:
            row[command_type] = int(to_parse.strip())
        elif "BAD_PEB_COUNT" in command_type:
            row[command_type] = int(to_parse.strip())
        elif "TOTAL_ERASE_BLOCKS" in command_type:
            row[command_type] = int(to_parse.strip())
        elif command_type == "VMSTAT":
            vm_stat_add_value(to_parse, row, command_type, success_command)
        elif command_type == "TEMPERATURE":
            row[command_type] = int(to_parse.split("\n")[1].split(":")[1].replace("'", "").strip())
        elif  "WIFI_CONFIG_CHANNEL" in command_type:
            row[command_type] = int(to_parse.split("\n")[1].split(":")[1].replace("'", "").strip())
        elif command_type == "REBOOT":
            row[command_type] = int(to_parse.split("\n")[1].split(":")[1].replace("'", "").strip())
        elif command_type == "FIRMWARE_VERSION":
            row[command_type] = to_parse.split("\n")[1].split(":")[1].replace("'", "").strip()
        elif command_type == "MODELE_NAME":
            row[command_type] = to_parse.split("\n")[1].split(":")[1].replace("'", "").strip()
        elif command_type == "VMZ_PS":
            parse_process_vmz(to_parse, row, logger)
        elif "CONNECTEDCLIENT" in command_type:
            row[command_type] = int(to_parse.split("\n")[0])
        elif command_type == "WIFI_CHANNEL_BH":
            row[command_type] = int(to_parse.split("\n")[1].split("\t")[1])
        elif command_type == "WIFI_CHANNEL_5G":
            row[command_type] = int(to_parse.split("\n")[1].split("\t")[1])
        elif command_type == "WIFI_CHANNEL_24G":
            row[command_type] = int(to_parse.split("\n")[1].split("\t")[1])
        elif command_type == "WIFI_BH_ASSOCLIST":
            parse_bh_assoclist(to_parse, row, command_type, success_command)
        elif "WIFI_CHANIM" in command_type:
            chanim_add_value(to_parse, row, command_type, success_command)
        elif command_type == "NB_CLIENT_WIFI_CONNECTED":
            row[command_type] = to_parse.split(" ")[0]
        elif "BACKHAUL_AP_RSSI_GENEMEXT" in command_type:
            row[command_type] = parse_wl_status(to_parse)
        elif "BACKHAUL_AP_" in command_type:
            myresultlst = to_parse.split("\n")
            for item in myresultlst:
                if 'value' in item:
                    row[command_type] = item.split(":")[1].replace("'", "").strip()
                    break
        elif "FS_SIZE" in command_type:
            row[command_type] = int(to_parse.split("\t")[0])
        elif "LOADAVG" in command_type:
            loadavg_add_value(to_parse, row, command_type, success_command)
        elif "DEVICE_STATUS" in command_type:
            row[command_type] =  to_parse.split("\n")
        elif "NB_HOSTAPD" in command_type:
            row[command_type] =  int(to_parse)
        elif "NB_DUMPCORE" in command_type:
            if "cat: can't open" in to_parse:
                row[command_type] = 0
            else:
                row[command_type] =  int(to_parse)
        elif "WIFI_BH_ASSOCLIST" == command_type:
            pass
        elif "PING_WO_DNS" in command_type:
            row[command_type] = parse_ping_wodns(to_parse)
        elif "TOP" in command_type:
            parse_top(to_parse, row)
        else :
            logger.error("Unknown command type %s", command_type)

    return row

def parse_sta_info(to_parse, sta_mac):
    """_summary_

    Args:
        to_parse (_type_): _description_
        sta_mac (_type_): _description_

    Returns:
        _type_: _description_
    """
    row = {}
    sta_info_list = to_parse.split("\n")
    for item in sta_info_list:
        if "tx failures:" in item:
            row['BH_STA_INFO_TX_FAILURES_'+sta_mac] = int(item.split(":")[1].strip(" "))
        if "link bandwidth =" in item:
            row['BH_STA_INFO_BANDWIDTH_'+sta_mac] = int(item.split("=")[1].split(" ")[1])
        if "in network " in item:
            #uptime = item.strip(" ").split(" ")
            row['BH_STA_INFO_UPTIME_'+sta_mac] = int(item.strip(" ").split(" ")[3])
        if "rx decrypt failures:" in item:
            row['BH_STA_INFO_DECRYPT_FAILURE_'+sta_mac] = int(item.split(":")[1].strip(" "))
    return row

def get_assoc_list_info(ip, username, password, bh_assoc_list, logger):
    """_summary_

    Args:
        ip (_type_): _description_
        username (_type_): _description_
        password (_type_): _description_
        bh_assoc_list (_type_): _description_
        logger (_type_): _description_

    Returns:
        _type_: _description_
    """
    row = {}
    if len(bh_assoc_list) == 0:
        return row
    for sta in bh_assoc_list:
        sta_mac = sta.split(" ")[1]
        command = "/usr/sbin/wlctl -i wl0.2 sta_info "+ sta_mac
        my_command = prepare_command(command, ip, username, password, logger)
        output, result = run_command(my_command, logger)
        if result is False:
            logger.error("Command : %s return %d : %S", my_command, result, output)

        row.update(parse_sta_info(output, sta_mac))
    return row

def do_extender_monitoring(network_list, network_setup, logger, system_command_lst, client):
    """This function launch per exender the list of commands. Then store the result into the file link to the extedner
    the system commande list is global.
    #TODO Don't forget to use the WiFi command too. Ands check how to deal with 2 differents lists

    Args:
        network_list (_type_): _description_
        network_setup (_type_): _description_
        logger (_type_): _description_
        system_command_lst (_type_): _description_
        client (_type_): _description_
    """
    command_to_execute = ""

    timestamp = datetime.datetime.utcnow().isoformat()
    serie = []
    device_serie = []
    #Parse the list of extenders
    for extender in network_list:
        rows = {}
        #rows['DATE'] = datetime.datetime.now()
        #For each extender launch the commands
        for command, command_type in system_command_lst:
            # For each command connect to extender and launch it
            command_to_execute = prepare_command(command, extender['ip'], extender['username'], extender['password'], logger)
            output, success_command = run_command(command_to_execute, logger)
            if command_type == 'WIFI_BH_ASSOCLIST':
                my_row = {}
                bh_assoc_list = parse_bh_assoclist(output, my_row, command_type, success_command)
                rows.update(my_row)
                my_row = get_assoc_list_info(extender['ip'], extender['username'], extender['password'], bh_assoc_list, logger)
                rows.update(my_row)
            rows.update(update_row(output, success_command, command_type, logger))

        tags = {'name' : extender['name'].strip(),
            'fw_version' : rows['FIRMWARE_VERSION'],
            'model_name' : rows['MODELE_NAME'],
            'setup': network_setup,
            'role' : extender['role'].strip()
            }

        extender_infux_db = {
            'time': timestamp,
            'measurement' : "MONITORING",
            'tags': tags,
            'fields' : rows,
        }
        #print ("TAGS {} FIELDS : {}".format(tags['name'], fields))
        serie.append(extender_infux_db)
        device_serie.extend(create_device_serie(extender,timestamp))

    #print ("SERIE : {} ".format(serie))
    #client.write_points(serie, time_precision='s',database="myDBExample")
    client.write(bucket="f266-em-controller", org="URDBBSSolution", record=serie)
    #client.write_points(device_serie, time_precision='s',database="myDBExample")
    client.write(bucket="f266-em-controller", org="URDBBSSolution", record=device_serie)
    return True

def monitoring_extenders(network_list, network_setup, polling_frequency, influxdb_server, dest_file, logger, system_command_lst):
    """Monitoring Extender poll for polling_frequency all the extender part of the network_list. Then will store the
    results into the dest_file in csv format.
    A dest_file will be created per extender, to allow to have different follow up

    Args:
        network_list (_type_): _description_
        network_setup (_type_): _description_
        polling_frequency (_type_): _description_
        influxdb_server (_type_): _description_
        dest_file (_type_): _description_
        logger (_type_): _description_
        system_command_lst (_type_): _description_
    """
    csv_header = []

    #Create CSV Header file
    csv_header.append('DATE')
    for command, command_type in system_command_lst:
        if "WIFI_CHANIM" in command_type:
            for chanim in chanim_info:
                csv_header.append(command_type + "-" + chanim)
        elif "VMSTAT" in command_type:
            for vmstat in vmstat_info:
                csv_header.append(command_type + "-" + vmstat)
        elif "LOADAVG" in command_type:
            for loadavg in loadavg_info:
                csv_header.append(command_type + "-" + loadavg)
        else:
            csv_header.append(command_type)
    #Create root file name by concatenating the root filename and the extender name
    for extender in network_list:
        extender_csv_name = dest_file +'-' + extender['name'].strip(" ") + ".csv"
        #Open the file
        if sys.version_info[0] == 2:
            extender_csv_file =  open(extender_csv_name, 'w+')
        else :
            extender_csv_file =  open(extender_csv_name, 'w+', encoding="utf-8")

        extender['CSVFile'] = extender_csv_file
        #Write header into csv files and define dictionary to manage and check row
        csv_writer = csv.DictWriter(extender['CSVFile'], fieldnames=csv_header)
        extender['CSVWriter'] = csv_writer
        extender['CSVWriter'].writeheader()
        logger.info("Creating file {:20} mode {:2}".format(extender['CSVFile'].name, extender['CSVFile'].mode))

    logger.info("Creating Data Base %s", influxdb_server["Server_name"])
    os.environ['NO_PROXY'] = influxdb_server["Server_name"]
    if sys.version_info[0] == 3:
        token = os.environ.get("INFLUXDB_TOKEN")
        org = influxdb_server["DB_name"]
        url = influxdb_server["Server_name"] + ":" + influxdb_server["Server_port"]
        influx_client = InfluxDBClient(url=url, token=token, org=org)
        client = influx_client.write_api(write_options=SYNCHRONOUS)
    elif sys.version_info[0] == 2:
        client = InfluxDBClient(host=influxdb_server["Server_name"],port=influxdb_server["Server_port"],
                                ssl=False, proxies=None)
    else:
        client = InfluxDBClient(url=influxdb_server["Server_name"], host=influxdb_server["Server_name"],port=influxdb_server["Server_port"],
                                ssl=False, proxies=None)

    if sys.version_info[0] <= 2:
        client.create_database(influxdb_server["DB_name"])
        logger.info("Creation of Data Base %s %s", influxdb_server["Server_name"], client.get_list_database())

    #Start looping for monitoring extender
    while 1:
        try:
            #Launch the command
            do_extender_monitoring(network_list, network_setup, logger, system_command_lst, client)
            #Sleep for polling frequency
            time.sleep(int(polling_frequency))

        except KeyboardInterrupt:
            #If Keyboard interruption then stop polling
            logger.info("KEYBOARD interrupt stop monitoring")
            break
        else:
            logger.debug("Out of polling wait launch commands")


    #End of monitoring close opened files
    for extender in network_list:
        logger.info("Closing file %s", extender['CSVFile'].name)
        extender['CSVFile'].close()

    return


def main(argv):
    """_summary_

    Args:
        argv (_type_): _description_

    Returns:
        _type_: _description_
    """
    logging.basicConfig(filename = "monitoring.log",
    level = logging.ERROR,
    format = LOG_FORMAT,
    filemode = 'w')

    logger = logging.getLogger()
    network_list = []
    system_command_list = []
    dest_file = ""
    polling_frequency = DEFAULT_POLLING_FREQUENCY
    args = ""
    try:
        opts, args = getopt.getopt(argv, "c:hf:d:vt:", ["config=","help", "frequency=", "destfile=", "verbose", "type="])
    except getopt.GetoptError:
        logger.error("Option error %s", args)
        print ("Option error")
        usage(argv)
        sys.exit(2)
    else:
        for option ,arg in opts:
            if option in ('-c', '--config'):
                logger.info("config file %s", arg)
                #network_list = openConfigFile(arg.strip(), logger)
                network_list = []
                if sys.version_info[0] == 2:
                    try:
                        with open (arg.strip(), 'r+') as config_file:
                            config_jsonlist = json.load(config_file)
                    except IOError:
                        logger.error("File %s does not exist", arg.strip())
                    else :
                        logger.debug("DUMP config file %s", network_list)
                else:
                    try:
                        with open (arg.strip(), 'r+', encoding="utf-8") as config_file:
                            config_jsonlist = json.load(config_file)
                    except IOError:
                        logger.error("File %s does not exist", arg.strip())
                    else :
                        logger.debug("DUMP config file %s", network_list)

            if option in ('-h', '--help'):
                usage(argv)
                return 0
            if option in ('-f', '--frequency'):
                try :
                    polling_frequency = int(arg)
                except ValueError:
                    logger.debug("Bad value for frequency parameter %s, force default value %d", arg, DEFAULT_POLLING_FREQUENCY)
                    polling_frequency = DEFAULT_POLLING_FREQUENCY
                else:
                    logger.info("Polling frequency %s", arg)
                finally:
                    pass

            if option in ('-d', '--destfile'):
                #Check if absolute file is use
                if ".." in arg:
                    print ("Use absolute path instead of relative path ")
                    usage(argv)

                if len(arg.split(".")) > 0:
                    dest_file = arg.split(".")[0]
                else:
                    dest_file = arg
                if "/" in dest_file:
                    #Extract path and file name. If directory does not exist then create directory if needed
                    path, file = os.path.split(os.path.abspath(dest_file))
                    index_path = 0
                    #To manage debugger issue with path management
                    if len (path.split(" ")) > 1:
                        index_path = 1
                    print ("%s %d %s %s", index_path, len (path.split(" ")), path.split(" "), file)

                    print ("%s %s %s", index_path, path.split(" ")[index_path], os.path.isdir(path.split(" ")[index_path]))
                    if os.path.isdir(path.split(" ")[index_path]) is False:
                        os.mkdir(path.split(" ")[index_path])
                logger.info("Destination file is : %s", dest_file)

            if option in ('-v','--verbose'):
                logger.setLevel(logging.DEBUG)

        if config_jsonlist["network_type"] == "F398BT":
            system_command_list = system_command_list_F398BT
        elif config_jsonlist["network_type"] == "F266GEN":
            system_command_list = system_command_list_F266GEN
        elif config_jsonlist["network_type"] == "F266GENEMEXT":
            system_command_list = system_command_list_F266GENEMEXT

        if len(config_jsonlist["network_config"]) == 0:
            print ("Config file is emty or not compliant")
            usage(argv)
            return -1
        if dest_file == "":
            print ("CSV Destination file is missing")
            usage(argv)
            return -1
        if len(system_command_list) == 0:
            print ("Need to define system type")
            usage (argv)
            return -1

        logger.info("Start monitoring with config file %s, destination file will be %s, polling frequency is %s network type %s", config_jsonlist["network_config"], dest_file, config_jsonlist["Frequency"], config_jsonlist["network_type"])
        monitoring_extenders(config_jsonlist["network_config"], config_jsonlist["network_type"],config_jsonlist["Frequency"], config_jsonlist["Influx_Server"], dest_file, logger, system_command_list)
    finally:
        pass
    return 0

if __name__ == "__main__":
    main(sys.argv[1:])

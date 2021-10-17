#!/usr/bin/python

import sys
import getopt
import logging
import csv
import time
import subprocess
import datetime
import os
from sys import version_info
if version_info[0] < 3:
#    from influxdb import InfluxDBClient
    print ("{}".format(version_info))
else :
    import influxdb_client
    from influxdb_client import InfluxDBClient, Point
    from influxdb_client.client.write_api import SYNCHRONOUS
    

from subprocess import STDOUT
#Local packages
from tools.config_file import *
from tools.tools import prepareCommand, runCommand

import json


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
["ps -aux", "VMZ_PS"]
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
["/usr/sbin/infos-cli -t OSM_MASTER_ELECTION -c all | grep ElecState", "ELEC_STATE"]
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
["du -s /opt/conf/datausage.db", "DATA_USAGE_FS_SIZE"]
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

chanim_info = ["chanspec", "tx", "inbss","obss","nocat","nopkt","doze","txop","goodtx","badtx","glitch","badplcp","knoise","idle","timestamp"]
vmstat_info = ["nb_process_running", "nb_process_sleep", "swap", "free", "buff", "cache", "si", "so", "bi", "bo", "interrupt", "context_switch", "user", "system", "idle","wait"]
loadavg_info = ["1MN", "5MN", "15MN"]
def usage(argv):
    print ("[-h, --help]: \t\tthis Message")
    print ("[-t, --type]: \tSystem type")
    print ("\t\t Supported type :")
    print ("\t\t F398BT --> BT F398")
    print ("\t\t F266GEN --> GENERIC F266")
    print ("[-c, --config]: \tMandatory Config file with the format")
    print ("\t\t\t@IP, ROLE, PLACE, LOGIN, PASSWORD")
    print ("[-f, --frequency]: \tOptional Polling frequency (default:{}s)".format(DEFAULT_POLLING_FREQUENCY))
    print ("[-d, --destfile]: \tMandatory root name of the CSV destination file") 
    print ("[-v, --verbose]: \tOptional set debug level mode") 

def parseElecState(to_parse):
    myListe = to_parse.split(",")
    elecState = myListe[0].split(" ")[1].strip("<").strip(">")
    return elecState

def getVMZ(ps_result, logger):
    try :
        index_status = ps_result.split(" ").index("R")
        logger.debug("{} -> Detect process in R")
    except ValueError:
        index_status = ps_result.split(" ").index("S")
        logger.debug("{} -> Detect process in S")
    finally:
        vmz_size = ps_result.split(" ")[index_status - 1]
        if "m" in vmz_size:
            vmz_size = vmz_size.replace("m", "000000")
        logger.debug("VMZ is {}".format(int(vmz_size)))
        return int(vmz_size)


def parseProcessVMZ2(output, row, logger):
    ps_list = output.split("\n")
    for ps_result in ps_list:
        if "hg6d" in ps_result:
            row["VMZ_HG6D"] = getVMZ(ps_result, logger)
        if "wshd" in ps_result:
            row["VMZ_WSHD"] = getVMZ(ps_result, logger)
        if "wstd" in ps_result:
            row["VMZ_WSTD"] = getVMZ(ps_result, logger)
        if "dhclient" in ps_result:
            row["VMZ_DHCLIENT"] = getVMZ(ps_result, logger)
        if "dhcrelay" in ps_result:
            row["VMZ_DHRELAY"] = getVMZ(ps_result, logger)
        if "ismd" in ps_result:
            row["VMZ_ISMD"] = getVMZ(ps_result, logger)
        if "dnsmasq" in ps_result:
            row["VMZ_DNSMASQ"] = getVMZ(ps_result, logger)
        if "hal_wifi" in ps_result:
            row["VMZ_HALWIFI"] = getVMZ(ps_result, logger)

''' deviceParseResult example of result
We can see on F@ST266 the foloowing result
    MACAddress : '74:e5:f9:f1:bc:6f'
    Name : 'rmm-p2100409pl'
    Active : 'true'
    RSSI : '-65'
    Layer1Interface : 'Device/WiFi/Radios/Radio[RADIO5G]'
    MACAddress : 'b8:27:eb:38:b3:93'
    Name : 'B8:27:EB:38:B3:93'
    Active : 'true'
    RSSI : '0'
    Layer1Interface : 'Device/WiFi/Radios/Radio[RADIO2G4]'
    MACAddress : 'B8:27:EB:54:83:86'
    Name : 'B8:27:EB:54:83:86'
    Active : 'false'
    RSSI : '0'
    Layer1Interface : 'Device/Ethernet/Interfaces/Interface[PHY2]'
    MACAddress : '58:E2:8F:19:CD:36'
    Name : 'iPhonedeFlorent'
    Active : 'false'
    RSSI : '-66'
    Layer1Interface : 'Device/WiFi/Radios/Radio[RADIO5G]'
    MACAddress : 'b0:0c:d1:5a:6f:6c'
    Name : 'CSM-9015427'
    Active : 'true'
    RSSI : '0'
    Layer1Interface : ''

On WHW2 here is the result :
    MACAddress : 'D8:F2:CA:89:CC:F4'
    Name : 'RMM-P2100723PW'
    Active : 'false'
    ConnectedDisc : ''
    RSSI : '-64'
    MACAddress : '5C:AA:FD:F0:94:9A'
    Name : 'SonosZP'
    Active : 'true'
    ConnectedDisc : 'Device/Services/BTServices/BTDiscsMgt/Discs/Disc[@uid='3']'
    RSSI : '-48'
    MACAddress : '78:28:CA:2A:A3:AA'
    Name : 'SonosZP'
    Active : 'true'
    ConnectedDisc : 'Device/Services/BTServices/BTDiscsMgt/Discs/Disc[@uid='1']'
    RSSI : '-70'
    MACAddress : 'B8:27:EB:6D:80:77'
    Name : 'pi-FRy'
    Active : 'true'
    ConnectedDisc : 'Device/Services/BTServices/BTDiscsMgt/Discs/Disc[@uid='1']'
    RSSI : '0'
    MACAddress : 'A4:6C:F1:0D:AD:9E'
    Name : 'Galaxy-A5-2017'
    Active : 'true'
    ConnectedDisc : 'Device/Services/BTServices/BTDiscsMgt/Discs/Disc[@uid='3']'
    RSSI : '-75'
    MACAddress : '9C:2E:A1:F9:26:2B'
    Name : 'Redmi5Plus-theomag'
    Active : 'true'
    ConnectedDisc : 'Device/Services/BTServices/BTDiscsMgt/Discs/Disc[@uid='2']'
    RSSI : '-52'

every sample has to be sent to the server
tag (MACADRESS)/tag (DeviceName)
field (active)
field (RSSI)
field (ConnectedDisc(only the UID of the DISC)
'''
def deviceParseResult(to_parse, extName, fwVersion, ModelName, client):
    timestamp = datetime.datetime.utcnow().isoformat()

    if len(to_parse) == 0:
        return 
    else:
        serie = []
        fields = {}
        while (True):
            try :
                elt = to_parse.pop(0)
            except IndexError :
                break

            if "MACAddress" in elt:
                macAddress = (elt.split("   MACAddress : ")[1].replace("'", ""))
                fields['MACAddress'] = macAddress
            if "Name" in elt:
                fields['Name'] = elt.split("   Name : ")[1].replace("'", "")
            if "Active" in elt:
                fields['Active'] = elt.split("   Active : ")[1].replace("'", "")
            if "ConnectedDisc" in elt:
                if (len(elt.split("   ConnectedDisc : ")[1].replace("'", "").split("=")) == 1):
                    fields['ConnectedDisc'] = "NA"
                else :
                    fields['ConnectedDisc'] = elt.split("   ConnectedDisc : ")[1].replace("'", "").split("=")[1].strip("]")
            if "RSSI" in elt:
                fields['RSSI'] = elt.split("   RSSI : ")[1].replace("'", "")
            if "Band" in elt:
                toSendToInfluxDevice = {}
                DeviceTags = {}
                fields['Band'] = elt.split("   Band : ")[1].replace("'", "")
                
                DeviceTags = {
                'MACAddress'    : macAddress,
                'DeviceName'    : fields['Name'],
                'name'          : extName,
                'fw_version'    : fwVersion,
                'model_name'    : ModelName
                }

                toSendToInfluxDevice = {
                'time' : timestamp,
                'measurement' : "DEVICE",
                'tags' : DeviceTags,
                'fields' : fields,
                }
                serie.append(toSendToInfluxDevice)
                
                # for myInflux in serie:
                #     print ("Envoie de la serie {}".format(myInflux))
                client.write_points(serie, time_precision='s',database="myDBExample")
                fields = {}            

    return 
# assoclist 10:D7:B0:1A:96:6F
# assoclist 10:D7:B0:1A:96:7B
def parseBHAssoclist(to_parse, row, command_type, success_command):
    if (len(to_parse) == 0):
        row[command_type] = 0
        return ""
    else:
        myList = to_parse.split("\n")
        del myList[-1]
        row[command_type] = len(myList)
        return (myList)
    
def chanimAddValue(to_parse, row, command_type, success_command):
    if success_command == True:
        chanim_answer = to_parse.split("\n")[2].split("\t")
        i = 0
        if (len(chanim_answer) < 1):
            i = 0
            for chanim in chanim_info:
                row[command_type + "-" + chanim] = -1
                i = i + 1
            return
        for chanim in chanim_info:
            try :
                chanim_answer[i].isdigit() 
            except IndexError:
                print ("Index Error {} {}".format(i, chanim_answer))
            else:
                if (chanim_answer[i].isdigit()):
                    row[command_type + "-" + chanim] = int(chanim_answer[i])
                elif (chanim_answer[i].isalnum()):
                    row[command_type + "-" + chanim] = 0 #chanim_answer[i]
                i = i + 1
    else:
        i = 0
        for chanim in chanim_info:
            row[command_type + "-" + chanim] = -1
            i = i + 1

def vmstatAddValue(to_parse, row, command_type, success_command):
    if success_command == True:
        vmstat_list = filter(lambda x: x != "", to_parse.split("\n")[2].split(" "))
        i = 0
        for vmstats in vmstat_info:
            row[command_type + "-" + vmstats] = int(vmstat_list[i])
            i = i + 1
    else:
        i = 0
        for vmstat in vmstat_info:
            row[command_type + "-" + vmstat] = -1
            i = i + 1

def loadavgAddValue(to_parse, row, command_type, success_command):
    if success_command == True:
        i = 0
        for loadavg in loadavg_info:
            row[command_type + "-" + loadavg] = float(to_parse.split(" ")[i])
            i = i + 1
    else:
        i = 0
        for loadavg in loadavg_info:
            row[command_type + "-" + loadavg] = float("0")
            i = i + 1


def updateRow(to_parse, success_command, command_type, logger):
    row = {}
    if success_command ==  False:
        if "WIFI_CHANIM" in command_type:
            chanimAddValue(to_parse, row, command_type, success_command)
        elif "VMSTAT" in command_type:
            vmstatAddValue(to_parse, row, command_type, success_command)
        elif "LOADAVG" in command_type:
            loadavgAddValue(to_parse, row, command_type, success_command)
        elif "BACKHAUL_AP_ID" in command_type :
            row[command_type] = "NA"
        elif "BACKHAUL_AP_TYPE" in command_type :
            row[command_type] = "NA"
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
        else:
            row[command_type] = -1
            logger.debug("Command {} failed".format(row))
    else :
        if command_type == "UPTIME":
            row[command_type] = float(to_parse.split(" ")[0])
            pass
        elif "ELEC_STATE" in command_type:
            row[command_type] = parseElecState(to_parse)
            pass
        elif "MEMINFO" in command_type :
            if to_parse.split(":")[1].strip().split(" ")[0].strip().isalnum() == True:
                row[command_type] = float(to_parse.split(":")[1].strip().split(" ")[0].strip())
            else :
                logger.error("Command type return non digit {} {}".format(to_parse.split(":")[1].strip().split(" ")[0].strip(),to_parse))
                row[command_type] = -1
            pass
        elif "MAX_EC" in command_type:
            row[command_type] = int(to_parse.strip())
            pass
        elif "BAD_PEB_COUNT" in command_type:
            row[command_type] = int(to_parse.strip())
            pass
        elif "TOTAL_ERASE_BLOCKS" in command_type:
            row[command_type] = int(to_parse.strip())
            pass
        elif command_type == "VMSTAT":
            vmstatAddValue(to_parse, row, command_type, success_command)
            pass
        elif command_type == "TEMPERATURE":
            row[command_type] = int(to_parse.split("\n")[1].split(":")[1].replace("'", "").strip())
            pass
        elif  "WIFI_CONFIG_CHANNEL" in command_type:
            row[command_type] = int(to_parse.split("\n")[1].split(":")[1].replace("'", "").strip())
            pass
        elif command_type == "REBOOT":
            row[command_type] = int(to_parse.split("\n")[1].split(":")[1].replace("'", "").strip())
            pass
        elif command_type == "FIRMWARE_VERSION":
            row[command_type] = to_parse.split("\n")[1].split(":")[1].replace("'", "").strip()
            pass
        elif command_type == "MODELE_NAME":
            row[command_type] = to_parse.split("\n")[1].split(":")[1].replace("'", "").strip()
            pass
        elif command_type == "VMZ_PS":
            parseProcessVMZ2(to_parse, row, logger)
        elif "CONNECTEDCLIENT" in command_type:
            row[command_type] = int(to_parse.split("\n")[0])
            pass
        elif command_type == "WIFI_CHANNEL_BH":
            row[command_type] = int(to_parse.split("\n")[1].split("\t")[1])
            pass
        elif command_type == "WIFI_CHANNEL_5G":
            row[command_type] = int(to_parse.split("\n")[1].split("\t")[1])
            pass
        elif command_type == "WIFI_CHANNEL_24G":
            row[command_type] = int(to_parse.split("\n")[1].split("\t")[1])
            pass
        elif command_type == "WIFI_BH_ASSOCLIST":
            parseBHAssoclist(to_parse, row, command_type, success_command)
        elif "WIFI_CHANIM" in command_type:
            chanimAddValue(to_parse, row, command_type, success_command)
        elif command_type == "NB_CLIENT_WIFI_CONNECTED":
            row[command_type] = to_parse.split(" ")[0]
        elif "BACKHAUL_AP_" in command_type:
            myresultlst = to_parse.split("\n")
            for item in myresultlst:
                if 'value' in item: 
                    row[command_type] = item.split(":")[1].replace("'", "").strip()
                    break
        elif "FS_SIZE" in command_type:
            row[command_type] = int(to_parse.split("\t")[0])
        elif "LOADAVG" in command_type:
            loadavgAddValue(to_parse, row, command_type, success_command)
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
        else :
            logger.error("Unknown command type {}".format(command_type))

    return row

def parseStaInfo(to_parse, macSta):
    row = {}
    staInfoList = to_parse.split("\n")
    for item in staInfoList:
        if ("tx failures:" in item):
            row['BH_STA_INFO_TX_FAILURES_'+macSta] = int(item.split(":")[1].strip(" "))
        if ("link bandwidth =" in item):
            row['BH_STA_INFO_BANDWIDTH_'+macSta] = int(item.split("=")[1].split(" ")[1])
        if ("in network " in item):
            uptime = item.strip(" ").split(" ")
            row['BH_STA_INFO_UPTIME_'+macSta] = int(item.strip(" ").split(" ")[3])
        if ("rx decrypt failures:" in item):
            row['BH_STA_INFO_DECRYPT_FAILURE_'+macSta] = int(item.split(":")[1].strip(" "))
    return row

def getAssoclistInfo(ip, username, password, BHAssoclist, logger):
    row = {}
    if (len(BHAssoclist) == 0):
        return row
    for STA in BHAssoclist:
        macSta = STA.split(" ")[1]
        command = "/usr/sbin/wlctl -i wl0.2 sta_info "+ macSta
        myCommand = prepareCommand(command, ip, username, password, logger)
        output, result = runCommand(myCommand, logger)
        row.update(parseStaInfo(output, macSta))
    return row


def DoExtenderMonitoring(network_list, network_setup, logger, system_command_lst, client):
    """This function launch per exender the list of commands. Then store the result into the file link to the extedner
    the system commande list is global.
    #TODO Don't forget to use the WiFi command too. Ands check how to deal with 2 differents lists
    """
    command_to_execute = ""

    timestamp = datetime.datetime.utcnow().isoformat()
    serie = []
    
    #Parse the list of extenders
    for extender in network_list:
        rows = {}
        #rows['DATE'] = datetime.datetime.now()
        #For each extender launch the commands
        for command, command_type in system_command_lst:
            # For each command connect to extender and launch it
            command_to_execute = prepareCommand(command, extender['ip'], extender['username'], extender['password'], logger)
            output, success_command = runCommand(command_to_execute, logger)
            if (command_type == 'WIFI_BH_ASSOCLIST'):
                myRow = {}
                BHAssocList = parseBHAssoclist(output, myRow, command_type, success_command)
                rows.update(myRow)
                myRow = getAssoclistInfo(extender['ip'], extender['username'], extender['password'], BHAssocList, logger)
                rows.update(myRow)
            rows.update(updateRow(output, success_command, command_type, logger))
        
        
        deviceParseResult(rows.pop("DEVICE_STATUS"), extender['name'].strip(), rows['FIRMWARE_VERSION'], rows['MODELE_NAME'], client)

        #extender['CSVWriter'].writerow(rows)
        logger.info("Write row {} in filen {}".format(rows, extender['CSVFile'].name))
        tags = {'name' : extender['name'].strip(),
            'fw_version' : rows['FIRMWARE_VERSION'],
            'model_name' : rows['MODELE_NAME'],
            'setup': network_setup,
            'role' : extender['role'].strip()
            }

        #print("EXTENDER NAME {} {}".format(extender.name, rows.items()))
        fields = {}
        
        # for key in rows.keys():
        #     if (key != 'DATE'):
        #         fields[key] = rows[key]

        extInfluxDB = {
            'time': timestamp,
            'measurement' : "MONITORING",
            'tags': tags,
            'fields' : rows,
        }
        #print ("TAGS {} FIELDS : {}".format(tags['name'], fields))
        serie.append(extInfluxDB)

    #print ("SERIE : {} ".format(serie))
    client.write_points(serie, time_precision='s',database="myDBExample")

def monitoringExtenders(network_list, network_setup, polling_frequency, influxServer, dest_file, logger, system_command_lst):
    extender_csv_file_list = []
    csv_header = []
    """Monitoring Extender poll for polling_frequency all the extender part of the network_list. Then will store the 
    results into the dest_file in csv format.
    A dest_file will be created per extender, to allow to have different follow up"""
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
        extender_csv_file =  open(extender_csv_name, 'w+')
        extender['CSVFile'] = extender_csv_file
        #Write header into csv files and define dictionary to manage and check row
        csv_writer = csv.DictWriter(extender['CSVFile'], fieldnames=csv_header)
        extender['CSVWriter'] = csv_writer
        extender['CSVWriter'].writeheader()
    
        logger.info("Creating file {:20} mode {:2}".format(extender['CSVFile'].name, extender['CSVFile'].mode))

    logger.info("Creating Data Base {}".format(influxServer["Server_name"])
    )
    os.environ['NO_PROXY'] = influxServer["Server_name"]
    client = InfluxDBClient(host=influxServer["Server_name"],port=influxServer["Server_port"], 
                            ssl=False, proxies=None)
    client.create_database(influxServer["DB_name"])
    logger.info("Creation of Data Base {} {}".format(influxServer["Server_name"], client.get_list_database()))
    
    #Start looping for monitoring extender
    while 1:
        try:
            #Launch the command
            DoExtenderMonitoring(network_list, network_setup, logger, system_command_lst, client)
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
        logger.info("Closing file {}".format(extender['CSVFile'].name))
        extender['CSVFile'].close()
        
    return


def main(argv):
    logging.basicConfig(filename = "monitoring.log",
    level = logging.ERROR,
    format = LOG_FORMAT,
    filemode = 'w')

    logger = logging.getLogger()
    network_list = []
    system_command_list = []
    dest_file = ""
    polling_frequency = DEFAULT_POLLING_FREQUENCY
    try:
        opts, args = getopt.getopt(argv, "c:hf:d:vt:", ["config=","help", "frequency=", "destfile=", "verbose", "type="])
    except getopt.GetoptError:
        logger.error("Option error");
        print ("Option error")
        usage(argv)
        sys.exit(2)    
    else:
        for option ,arg in opts:
            if option in ('-c', '--config'):
                logger.info("config file {}".format(arg))
                #network_list = openConfigFile(arg.strip(), logger)
                network_list = []
                try:
                    with open (arg.strip(), 'r+') as configFile:
                        config_jsonlist = json.load(configFile)
                except IOError:
                    logger.error("File {} does not exist".format(arg.strip()))
                else :
                    logger.debug("DUMP config file {} ".format(network_list))

            if option in ('-h', '--help'):
                usage(argv)
                return 0
            if option in ('-f', '--frequency'):
                try :
                    polling_frequency = int(arg)
                except ValueError:
                    logger.debug("Bad value for frequency parameter {}, force default value {}".format(arg, DEFAULT_POLLING_FREQUENCY))
                    polling_frequency = DEFAULT_POLLING_FREQUENCY
                else:
                    logger.info("Polling frequency {}".format(arg))
                finally:
                    pass

            if option in ('-d', '--destfile'):
                #Check if absolute file is use
                if (".." in arg):
                    print ("Use absolute path instead of relative path ")
                    usage(argv)

                if (len(arg.split(".")) > 0):
                    dest_file = arg.split(".")[0]
                else:
                    dest_file = arg
                
                if ("/" in dest_file):           
                    #Extract path and file name. If directory does not exist then create directory if needed
                    path, file = os.path.split(os.path.abspath(dest_file))
                    index_path = 0
                    #To manage debugger issue with path management
                    if (len (path.split(" ")) > 1):
                        index_path = 1
                    print ("{} {} {}".format(index_path, len (path.split(" ")), path.split(" ")))

                    print ("{} {} {}".format(index_path, path.split(" ")[index_path], os.path.isdir(path.split(" ")[index_path])))
                    if (os.path.isdir(path.split(" ")[index_path]) == False):
                        os.mkdir(path.split(" ")[index_path])
                logger.info("Destination file is : {}".format(dest_file))

            if option in ('-v','--verbose'):
                logger.setLevel(logging.DEBUG)

        if (config_jsonlist["network_type"] == "F398BT"):
            system_command_list = system_command_list_F398BT
        elif (config_jsonlist["network_type"] == "F266GEN"):
            system_command_list = system_command_list_F266GEN
 
        if (len(config_jsonlist["network_config"]) == 0):
            print ("Config file is emty or not compliant")
            usage(argv)
            return -1
        if (dest_file == ""):
            print ("CSV Destination file is missing")
            usage(argv)
            return -1
        if (len(system_command_list) == 0):
            print ("Need to define system type")
            usage (argv)
            return -1

        logger.info("Start monitoring with config file {}, destination file will be {}, polling frequency is {} network type {}".format(config_jsonlist["network_config"], dest_file, config_jsonlist["Frequency"], config_jsonlist["network_type"]))
        monitoringExtenders(config_jsonlist["network_config"], config_jsonlist["network_setup"],config_jsonlist["Frequency"], config_jsonlist["Influx_Server"], dest_file, logger, system_command_list)
    finally:

        pass

if __name__ == "__main__":
        main(sys.argv[1:])

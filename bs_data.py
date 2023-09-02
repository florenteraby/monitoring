#!/usr/bin/python
# coding: utf-8
"""_summary_

    Returns:
        _type_: _description_
"""
import logging
from tools import tools

bs_data_command = [
    ["/usr/sbin/wlctl -i wl0.1 bs_data", "wl0.1"],
    ["/usr/sbin/wlctl -i wl0.3 bs_data", "wl0.3"], 
    ["/usr/sbin/wlctl -i wl1 bs_data", "wl1"]
]

""" 
  Station Address   PHY Mbps  Data Mbps    Air Use   Data Use    Retries    bw   mcs   Nss   ofdma mu-mimo 
DA:56:05:7B:FD:2B     1200.9        0.0       0.0%      30.5%       0.0%    80    11     2    0.0%    0.0% 
50:84:92:F1:1A:44     1200.9        0.0       0.1%      69.5%       0.0%    80    11     2    0.0%    0.0% 
        (overall)          -        0.0       0.1%         -         -
"""

def parse_bs_data(bs_data_result, bs_data_logger):
    """Parse the result of the command for one radio. Then create list of samples to send to InfluxDB

    Args:
        bs_data_result (string): the result of the command
        bs_data_logger (logger): the logger

    Returns:
        list: list of bs_data sample to send to the InfluxDB
    """
    bs_data_sample = []
    lines = bs_data_result.split("\n")
    for line in lines:
        sample = {}
        station_stats = line.split("  ")
        station_stats = list(filter(None, station_stats))
        if len(station_stats) > 1 and station_stats[0] != "Station Address" and station_stats[0] != "(overall)":
            bs_data_logger.debug("The station to parse : %s", station_stats[0])
            try :
                retries = float(station_stats[5].split("%")[0])
            except ValueError:
                bs_data_logger.debug("ValueError : %s", station_stats[0])
                retries = -1
            bs_data_logger.debug("nb of retries %d", retries)

            station = station_stats[0]
            sample = {
                'station' : station,
                'retries' : retries
            }
            bs_data_sample.append(sample)
        else:
            bs_data_logger.debug("First line or last line (skip it) : %s", station_stats)


    return bs_data_sample

def create_bs_data_series(extender, timestamp):
    """Create the serie of sample tagged to the InfluxDB

    Args:
        extender (extender def): extender definition
        timestamp (timestamp): 

    Returns:
        list: series to be sent to InfluxDB
    """
    bs_data_series_list = []
    bs_data_logger = logging.getLogger()

    for command, interface in bs_data_command:
        to_execute = tools.prepare_command(command, extender['ip'], extender['username'], extender['password'], bs_data_logger)
        bs_data_result, success = tools.run_command(to_execute, bs_data_logger)
        if success is True:
            bs_data_logger.debug("command %s : success %s result : %s", to_execute, success, bs_data_result)

            bs_data_sample = parse_bs_data(bs_data_result, bs_data_logger)
            for sample in bs_data_sample:
                bs_data_tags = {
                    'name' : extender['name'].strip(),
                    'interface' : interface,
                    'station' : sample.get('station')
                }

                bs_data_serie = {
                    'time' : timestamp,
                    'tag' : bs_data_tags,
                    'measurement' : "STATION_BSS",
                    'fields' : sample
                }
                bs_data_series_list.append(bs_data_serie)
        else:
            bs_data_logger.error("Error on collecting the commande : %s : %s", to_execute, bs_data_result)

    return bs_data_series_list

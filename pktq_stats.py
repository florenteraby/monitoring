#!/usr/bin/python
# coding: utf-8
"""_summary_

    Returns:
        _type_: _description_
"""

import logging
from tools import tools

pktq_stats_command_list = [
    ["/usr/sbin/wlctl -i wl0 pktq_stats", "wl0"],
    ["/usr/sbin/wlctl -i wl1 pktq_stats", "wl1"]
]

def pktq_stats_update_sample(data, queue, index):
    """Fill the sample data to prepare InfluxDB

    Args:
        data (list): Data 
        queue (string): String of the queue
        index (_type_): Index of the queue

    Returns:
        _type_: the sample
    """

    sample = {
        'queue' : queue,
        'index' : int(index),
        'dropped' : int(data[2].strip()),
        'retried' : int(data[3].strip()),
        'rtsfail' : int(data[4].strip()), 
        'rtrydrop' : int(data[5].strip()),
        'psretry' : int(data[6].strip())
    }
    return sample

def parse_pktq_stats(result, parse_pktq_stats_logger):
    """_summary_

    Args:
        result (_type_): _description_
        parse_pktq_stats_logger (_type_): _description_

    Returns:
        _type_: _description_
    """
    queue_list = []
    queue = {}

    pktq_stats_lines = result.split("\n")
    for pktq_stats_line in pktq_stats_lines:
        line = pktq_stats_line.split(":")
        if len(line) > 1:
            parse_pktq_stats_logger.debug("Proceed the parsing of %s", line)
            index = line[0]
            if index != 'prec':
                data = line[1].replace("-", "-1").split(",")
                bk_q = data[0].split('BK')
                if len(bk_q) > 1:
                    parse_pktq_stats_logger.debug("Parsing data %s", bk_q)
                    queue = pktq_stats_update_sample(data, 'bk', index)
                    parse_pktq_stats_logger.debug("Create sample %s", queue)
                    queue_list.append(queue)
                else:
                    be_q = data[0].split('BE')
                    if len (be_q) > 1 :
                        parse_pktq_stats_logger.debug("Parsing data %s", be_q)
                        queue = pktq_stats_update_sample(data, 'be', index)
                        parse_pktq_stats_logger.debug("Create sample %s", queue)
                        queue_list.append(queue)
                    else:
                        vi_q = data[0].split('VI')
                        if len(vi_q) > 1:
                            parse_pktq_stats_logger.debug("Parsing data %s", vi_q)
                            queue = pktq_stats_update_sample(data, 'vi', index)
                            parse_pktq_stats_logger.debug("Create sample %s", queue)
                            queue_list.append(queue)

                        else :
                            vo_q = data[0].split('VO')
                            if len(vo_q) > 1:
                                parse_pktq_stats_logger.debug("Parsing data %s", vo_q)
                                queue = pktq_stats_update_sample(data, 'vo', index)
                                parse_pktq_stats_logger.debug("Create sample %s", queue)
                                queue_list.append(queue)

                            else :
                                parse_pktq_stats_logger.errot("Nothing to parse %s", data)
            else:
                parse_pktq_stats_logger.debug("Skip the 1st line of the table %s", line[1])
        else:
            parse_pktq_stats_logger.debug("Should be the 1st line %s drop it", line)

    return queue_list

def create_pktq_stats_series(extender, timestamp):
    """Create and initiate the pktq_stats on all available interface. That allow to gather stats which can help to identify issue

    Args:
        extender (extender): extender definition to connect to the extender
        timestamp (timestamp): timestamp
    """
    pktq_serie_list = []
    pktq_stats_logger = logging.getLogger()
    for command, interface in pktq_stats_command_list:
        to_execute = tools.prepare_command(command, extender['ip'], extender['login'], extender['password'], pktq_stats_logger)
        pktq_stats_logger.debug("%s", to_execute)
        pktq_result, success = tools.run_command(to_execute, pktq_stats_logger)
        pktq_stats_logger.debug("success: %s : result : %s ", success, pktq_result)
        if success is True:
            pktq_sample = parse_pktq_stats(pktq_result, pktq_stats_logger)
            pktq_tags = {
                'name' : extender['name'].strip(),
                'interface' : interface
            }
            pktq_serie = {
                'time' : timestamp,
                'tag' : pktq_tags,
                'measurement' : "EXTENDER_PKTQ",
                'fields' : pktq_sample
            }
            pktq_serie_list.append(pktq_serie)
        else :
            pktq_stats_logger.error("Cannot get result for command : %s \n Result is %s\n", command, pktq_result)

    return pktq_serie_list

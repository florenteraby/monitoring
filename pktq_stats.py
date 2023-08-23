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

"""
common queue
prec:(AC)    rqstd,  stored, dropped, retried, rtsfail,rtrydrop, psretry,    acked,utlsn,data Mbits, phy Mbits,%nss 1/2/3/4,  %air, %effcy  (v6)
  00: BK         0,       0,       0,       0,       0,       0,       0,        0,    0,      0.00,      0.00,  -/ -/ -/ -,   0.0,    0.0
  01: BK         0,       0,       0,       -,       -,       0,       0,        0,    0,         -,         -,           -,     -,      -
  02: BK         0,       0,       0,       0,       0,       0,       0,        0,    0,      0.00,      0.00,  -/ -/ -/ -,   0.0,    0.0
  03: BK         0,       0,       0,       -,       -,       0,       0,        0,    0,         -,         -,           -,     -,      -
  04: BE    285087,  285087,       0,       0,       0,       0,       0,        0,   56,      0.00,      0.00,  -/ -/ -/ -,   0.0,    0.0
  05: BE         0,       0,       0,       -,       -,       0,       0,        0,    0,         -,         -,           -,     -,      -
  06: BE         0,       0,       0,       0,       0,       0,       0,        0,    0,      0.00,      0.00,  -/ -/ -/ -,   0.0,    0.0
  07: BE         0,       0,       0,       -,       -,       0,       0,        0,    0,         -,         -,           -,     -,      -
  08: VI         0,       0,       0,       0,       0,       0,       0,        0,    0,      0.00,      0.00,  -/ -/ -/ -,   0.0,    0.0
  09: VI         0,       0,       0,       -,       -,       0,       0,        0,    0,         -,         -,           -,     -,      -
  10: VI         0,       0,       0,       0,       0,       0,       0,        0,    0,      0.00,      0.00,  -/ -/ -/ -,   0.0,    0.0
  11: VI         0,       0,       0,       -,       -,       0,       0,        0,    0,         -,         -,           -,     -,      -
  12: VO    230157,  230157,       0,       0,       0,       0,       0,        0,    2,      0.00,      0.00,  -/ -/ -/ -,   0.0,    0.0
  13: VO         0,       0,       0,       -,       -,       0,       0,        0,    0,         -,         -,           -,     -,      -
  14: VO         0,       0,       0,      42,       0,       6,       0,        1,    0,      0.00,      6.00,  -/ -/ -/ -,   0.0,    1.9
  15: VO        60,      60,       0,       -,       -,       0,       0,        0,    0,         -,         -,           -,     -,      -
"""
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
                data = line[1].split(",")
                bk = data[0].split('BK')
                if len(bk) > 1:
                    parse_pktq_stats_logger.debug("Parsing data %s", bk)
                    queue = {
                        'queue' : 'bk',
                        'index' : int(index),
                        'dropped' : data[2].strip(),
                        'retried' : data[3].strip(),
                        'rtsfail' : data[4].strip(), 
                        'rtrydrop' : data[5].strip(),
                        'psretry' : data[6].strip()
                    }
                    parse_pktq_stats_logger.debug("Create sample %s", queue)
                    queue_list.append(queue)
                else:
                    be = data[0].split('BE')
                    if len (be) > 1 :
                        parse_pktq_stats_logger.debug("Parsing data %s", be)
                        queue = {
                            'queue' : 'be',
                            'index' : int(index),
                            'dropped' : data[2].strip(),
                            'retried' : data[3].strip(),
                            'rtsfail' : data[4].strip(), 
                            'rtrydrop' : data[5].strip(),
                            'psretry' : data[6].strip()
                        }
                        parse_pktq_stats_logger.debug("Create sample %s", queue)
                        queue_list.append(queue)
                    else:
                        vi = data[0].split('VI')
                        if len(vi) > 1:
                            parse_pktq_stats_logger.debug("Parsing data %s", vi)
                            queue = {
                                'queue' : 'vi',
                                'index' : int(index),
                                'dropped' : data[2].strip(),
                                'retried' : data[3].strip(),
                                'rtsfail' : data[4].strip(), 
                                'rtrydrop' : data[5].strip(),
                                'psretry' : data[6].strip()
                            }
                            parse_pktq_stats_logger.debug("Create sample %s", queue)
                            queue_list.append(queue)

                        else :
                            vo = data[0].split('VO')
                            if len(vo) > 1:
                                parse_pktq_stats_logger.debug("Parsing data %s", vi)
                                queue = {
                                    'queue' : 'vo',
                                    'index' : int(index),
                                    'dropped' : data[2].strip(),
                                    'retried' : data[3].strip(),
                                    'rtsfail' : data[4].strip(), 
                                    'rtrydrop' : data[5].strip(),
                                    'psretry' : data[6].strip()
                                }
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

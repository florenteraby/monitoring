#!/usr/bin/python

"""The purpose of this script is to check if the URL for download change.
It is really specific to my setup. 
The idea is to use cron mecanism on the pi to launch the script
"""
import json
import sys
import logging
import getopt

LOG_FORMAT = "%(levelname)s %(asctime)s %(funcName)s- %(message)s"
DEFAULT_POLLING_FREQUENCY = 600

def usage(argv):
    """[Usage of the scripts]

    Args:
        argv ([type]): [description]
    """
    print("Usage ")
    print ("[-h, --help]: \t\tthis Message")
    print ("[-c, --config]: \tMandatory Config file with the format")

def check_upgrade_url(discList_json):
    """[summary]

    Args:
        discList_json ([List]): [List of disc we need to check the upgrade URL]

    Returns:
        [BOOL]: [False no disc in the list, or the 
                 True Disc list is not empty and action was done OK]
    """
    if len(discList_json) == 0 :
        return False
    
    for disc in discList_json:
        print("Disc {}".format(disc))
    return True
        

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
        opts, args = getopt.getopt(argv, "c:h:", ["config=","help"])
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

        check_upgrade_url(config_jsonlist["network_config"])

if __name__ == "__main__":
        main(sys.argv[1:])



#!/usr/bin/python

"""The purpose of this script is to check if the URL for download change.
It is really specific to my setup. 
The idea is to use cron mecanism on the pi to launch the script
"""
import json
import sys
import logging
import getopt
from monitor import prepareCommand, runCommand


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
    print ("[-v, --v]: \tverbosity in log file")

URL_LOCAL_SUOTA = "http://pi-fry.home/TEST2/WHW6"
def check_url_output(current_url):
    """[This fontion check if the URL in parameter is the expected to allow dedicated upgrade SUOTA]

    Args:
        current_url ([string]): [The URL read ]

    Returns:
        [BOOL]: [True  : URL is the one expected]
                [False : URL is not the one expected]
    """
    try:
        read_url = current_url.decode('utf8').split("value : ")[1].strip().replace("'", "")
    except IndexError:
        return False
    else :
        if (read_url != URL_LOCAL_SUOTA):
            return False
        else:
            return True

check_command = "xmo-client -p Device/Services/AdvancedFwUpdate/URL"
def check_url_set_to(disc, url_to_set, logger):
    """[Set the url to the one in parameter on the disc/extender]

    Args:
        url_to_set ([string]): [URL to configure]
        disc
    """
    command_to_set = check_command + " -s " + url_to_set
    cmd = prepareCommand(command_to_set, disc['ip'], disc['username'], disc['password'], logger)
    output, cmdSuccess = runCommand(cmd,logger)
    logger.debug("Execute cmd {} \n\t Result of the commande {} {}".format(cmd, output, cmdSuccess))
    if (cmdSuccess == False):
        logger.error("Cannot execute command {} : {}".format(cmd, output))
        

def check_upgrade_url(discList_json, logger):
    """[summary]

    Args:
        discList_json ([List]): [List of disc we need to check the upgrade URL]
        logger

    Returns:
        [BOOL]: [False no disc in the list, or the 
                [True Disc list is not empty and action was done OK]
    """
    if (len(discList_json) == 0 ):
        logger.debug("Disc list is empty : {}".format(len(discList_json)))
        return False
    
    for disc in discList_json:
        logger.debug("Disc {}".format(disc))
        cmd = prepareCommand(check_command, disc["ip"],disc["username"], disc["password"], logger)
        outputCmd, successCmd = runCommand(cmd, logger)
        if (successCmd == True):
            if (check_url_output(outputCmd) == False):
                logger.info("Need to change URL {}".format(URL_LOCAL_SUOTA))
                check_url_set_to(disc, URL_LOCAL_SUOTA, logger)
            else :
                logger.debug("No need to change the URL {}".format(outputCmd))
        else:
            logger.debug("Command failed : {} - {}".format(cmd, outputCmd))
    return True
        

def main(argv):
    logging.basicConfig(filename = "check_url.log",
    level = logging.ERROR,
    format = LOG_FORMAT,
    filemode = 'w')

    logger = logging.getLogger()
    network_list = []
    run = False
    system_command_list = []
    dest_file = ""
    polling_frequency = DEFAULT_POLLING_FREQUENCY
    try:
        opts, args = getopt.getopt(argv, "c:hv", ["config=","help", "v"])
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
                    with open (arg, 'r+') as configFile:
                        config_jsonlist = json.load(configFile)
                        run = True
                except IOError:
                    logger.error("File {} does not exist".format(arg.strip()))
                else :
                    logger.debug("DUMP config file {} ".format(network_list))

            if option in ('-h', '--help'):
                usage(argv)
                return 0

            if option in ('-v', '--v'):
                logger.setLevel(logging.DEBUG)
            

        if (run == True):
            check_upgrade_url(config_jsonlist["network_config"], logger)
        else :
            usage(argv)

if __name__ == "__main__":
        main(sys.argv[1:])



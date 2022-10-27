#!/usr/bin/python

"""The purpose of this script is to check if the URL for download change.
It is really specific to my setup.
The idea is to use cron mecanism on the pi to launch the script
"""
import json
import sys
import logging
import getopt
#from tools.tools import prepareCommand, runCommand
import tools.tools

LOG_FORMAT = "%(levelname)s %(asctime)s %(funcName)s- %(message)s"
DEFAULT_POLLING_FREQUENCY = 600


CHECK_COMMAND = "xmo-client -p "
class check_xpath_class:
    """[Class check_xpath_class : Allow to check if a xpa]
    """
    def __init__(self, xpath, expected_value):
        self.xpath = xpath
        self.expected_value = expected_value

    def check_xpath(self, disc):
        """[check if the xPath get the expected value]

        Args:
            disc ([Json Disc]): [IP, UserName, Password to connect to the extender]
        """
        check_command = CHECK_COMMAND + self.xpath
        #"""Prepare the command to run, should contain xmo-client -p then add the expected xpath """
        cmd = tools.tools.prepareCommand(check_command, disc["ip"],disc["username"], disc["password"], logging.getLogger())
        #""""Call the prepare command fonction to get the fulll sshpass"""
        output_cmd, success_cmd = tools.tools.runCommand(cmd, logging.getLogger())
        #""""Run the command"""
        if (success_cmd is True):
            #""""if the command success we can parse the result"""
            try:
                read_value = output_cmd.decode('utf8').split("value : ")[1].strip().replace("'", "")
            except IndexError:
                return False
            else :
                if (read_value != self.expected_value):
                    #""""Compare with the expected result"""
                    return False
                else:
                    return True
        else:
            #""""Command is not successful, log it"""
            logging.getLogger().error("Command : %s Failed\n\t%s", cmd, output_cmd)
            return False

    def set_expected_value(self, disc):
        """[Set the expected on the  on disc]

        Args:
            disc ([Json Disc]): [IP, UserName, Password to connect to the extender]
        """
        set_command = CHECK_COMMAND + self.xpath +" -s " + self.expected_value
        #Prepare the command to set the expected value
        cmd = tools.tools.prepareCommand(set_command, disc["ip"],disc["username"], disc["password"], logging.getLogger())

        output_cmd, success_cmd = tools.tools.runCommand(cmd, logging.getLogger())
        #Execute the command
        if (success_cmd is False):
            #Log if the command is not successfull
            logging.getLogger().error("Command : {%s} Failed\n\t{%s}".format(cmd, output_cmd))
        return success_cmd


def usage(argv):
    """[Usage of the scripts]

    Args:
        argv ([type]): [description]
    """
    print("Usage ")
    print ("[-h, --help]: \t\tthis Message")
    print ("[-c, --config]: \tMandatory Config file with the format")
    print ("[-v, --v]: \tverbosity in log file")

def check_xpath(disc_list_json, xpath2check_json, logger):
    """[summary]

    Args:
        discList_json ([List]): [List of disc we need to check the upgrade URL]
        xpath2check_json ([List] : [List of xpath and value we need to check])
        logger

    Returns:
        [BOOL]: [False no disc in the list, or the
                [True Disc list is not empty and action was done OK]
    """
    if (len(disc_list_json) == 0 or len(xpath2check_json) == 0):
        logger.debug("Disc list is empty : {%d}".format(len(disc_list_json)))
        return False

    for disc in disc_list_json:
        logger.debug("Disc {}".format(disc))
        for xpath2check in xpath2check_json:
            xpath_check = check_xpath_class(xpath2check['xpath'], xpath2check['expected_value'])
            if (xpath_check.check_xpath(disc) is False):
                xpath_check.set_expected_value(disc)
            else:
                logger.info("No Change needed")
            del xpath_check
    return True


def main(argv):
    """_summary_

    Args:
        argv (_type_): _description_

    Returns:
        _type_: _description_
    """
    logging.basicConfig(filename = "check_url.log",
    level = logging.ERROR,
    format = LOG_FORMAT,
    filemode = 'w')

    logger = logging.getLogger()
    network_list = []
    run = False
    try:
        opts, args = getopt.getopt(argv, "c:hv", ["config=","help", "v"])
    except getopt.GetoptError:
        logger.error("Option error")
        print ("Option error")
        usage(argv)
        sys.exit(2)
    else:
        for option ,arg in opts:
            if option in ('-c', '--config'):
                logger.info("config file {%s}".format(arg))
                #network_list = openConfigFile(arg.strip(), logger)
                try:
                    with open (arg, 'r+') as config_file:
                        config_jsonlist = json.load(config_file)
                        run = True
                except IOError:
                    logger.error("File {} does not exist".format(arg.strip()))
                else :
                    logger.debug("DUMP config file {%s} ".format(network_list))

            if option in ('-h', '--help'):
                usage(argv)
                run = False

            if option in ('-v', '--v'):
                logger.setLevel(logging.DEBUG)

        if (run is True):
            check_xpath(config_jsonlist["network_config"], config_jsonlist["check_xpath"],logger)
        else :
            usage(argv)

        return run

if __name__ == "__main__":
    main(sys.argv[1:])

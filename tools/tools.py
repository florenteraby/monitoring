#!/usr/bin/python

import sys
import subprocess
import logging
from subprocess import STDOUT


def prepareCommand(command, ip, login, password, logger):
    command_to_execute = "/usr/bin/sshpass -p"+password.strip()+" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=3 -o ConnectionAttempts=2 "+login.strip()+"@"+ip.strip()+" "+command
    logger.debug("Command to execute {}".format(command_to_execute))
    return command_to_execute

def runCommand(command, logger):
    success_command = False
    try:
        # output = subprocess.check_output(command.split(" "), stderr=STDOUT, timeout=30)
        output = subprocess.check_output(command.split(" "), stderr=STDOUT)
    except subprocess.CalledProcessError as error_exec:
        logger.error("{} -> {}".format(error_exec.cmd, error_exec.output))
        output = error_exec.output
    # except subprocess.TimeoutExpired as error_exec:
    #     logger.error("{} -> {}".format(error_exec.cmd, error_exec.output))
    #     output = error_exec.output
    else:
        logger.info("{}\n".format (output))
        success_command = True
    finally:
        return output, success_command

def main(argv):
    return True

    
if __name__ == "__main__":
        main(sys.argv[1:])

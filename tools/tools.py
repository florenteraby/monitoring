#!/usr/bin/python

import sys
import subprocess
from subprocess import STDOUT


def prepare_command(command, ip, login, password, logger):
    """_summary_

    Args:
        command (_type_): _description_
        ip (_type_): _description_
        login (_type_): _description_
        password (_type_): _description_
        logger (_type_): _description_

    Returns:
        _type_: _description_
    """
    command_to_execute = "/usr/bin/sshpass -p"+password.strip()+" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=3 -o ConnectionAttempts=2 "+login.strip()+"@"+ip.strip()+" "+command
    logger.debug("Command to execute {}".format(command_to_execute))
    return command_to_execute

def run_command(command, logger):
    """_summary_

    Args:
        command (_type_): _description_
        logger (_type_): _description_

    Returns:
        _type_: _description_
    """
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
        return output.decode('utf8'), success_command

def main(argv):
    """_summary_

    Args:
        argv (_type_): _description_

    Returns:
        _type_: _description_
    """
    return True

if __name__ == "__main__":
    main(sys.argv[1:])

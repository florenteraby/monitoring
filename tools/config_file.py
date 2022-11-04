

class NetworkConfig:
    """_summary_
    """
    def __init__(self, config):
        self.ip = config.split(",")[0]
        self.role = config.split(",")[1]
        self.name = config.split(",")[2]
        self.login = config.split(",")[3]
        self.password = config.split(",")[4]
        self.csv_file = ""
        self.csv_writer = ""

    def set_csv_file(self, csv_file):
        """_summary_

        Args:
            csv_file (_type_): _description_
        """
        self.csv_file = csv_file

    def set_csv_writer(self, csv_writer):
        """_summary_

        Args:
            csv_writer (_type_): _description_
        """
        self.csv_writer = csv_writer

    def display(self):
        """_summary_
        """
        print("Name %S Role %S IP %s Login %s", self.name, self.role, self.ip, self.login)
    def log(self, logger):
        """_summary_

        Args:
            logger (_type_): _description_
        """
        logger.debug("Name {:12}\tRole {} \tIP {:15} \tLogin {}\tCSV {}".format(self.name, self.role, self.ip, self.login, self.csv_file.name))


def config_log_list(config_list, logger):
    """_summary_

    Args:
        config_list (_type_): _description_
        logger (_type_): _description_
    """
    for network_config in config_list:
        network_config.log(logger)

def open_config_file(filename, logger):
    """Function wihch parse the config file for monitoring WHW solution.
    File has to build as follow :
    @IP of the extender,
    ROLE [MASTER or SLAVE]
    NAME
    Login
    Password,
    All separated by comma"""
    network_list = []
    try:
        config = open(filename,'r+', encoding="utf-8")

    except IOError:
        print ("File {} does not exist".format(filename))
        logger.error("File does not exist {}".format(filename))
    else:
        network_config = config.readlines()
        for line in network_config:
            network = NetworkConfig(line)
            network_list.append(network)

        config.close()
    finally:
        logger.info("Number of devices {}".format(len(network_list)))
        return network_list


def main():
    """_summary_
    """
    pass


if __name__ == "__main__":
    main()

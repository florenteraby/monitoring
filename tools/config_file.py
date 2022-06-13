

class NetworkConfig:
    def __init__(self, config):
        self.ip = config.split(",")[0]
        self.role = config.split(",")[1]
        self.name = config.split(",")[2]
        self.login = config.split(",")[3]
        self.password = config.split(",")[4]
    def setCSVFile(self, csv_file):
        self.csvfile = csv_file
    def setCSVWriter(self, csv_writer):
        self.csvWriter = csv_writer

    def display(self):
        print("Name {} Role {} IP {} Login {}".format(self.name, self.role, self.ip, self.login))
    def log(self, logger):
        logger.debug("Name {:12}\tRole {} \tIP {:15} \tLogin {}\tCSV {}".format(self.name, self.role, self.ip, self.login, self.csvfile.name))


def ConfigLoglist(config_list, logger):
    for network_config in config_list:
        network_config.log(logger)    

def openConfigFile(filename, logger):
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
        config = open(filename,'r+')
        
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
    pass


if __name__ == "__main__":
        main()
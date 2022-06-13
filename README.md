# monitoring
Monitor extenders setup

The configuration file example 
JSON file

node  mandatory for monitor.py and check_xpath.py: 
"network_config". This node describe the network configuration of the network, it contains the list of devices to monitor.
List of configuration must have :
- "ip" : IP address of the device
- "role" : The role of the device
- "name" : Name to display on KIBANA
- "username" : Login name
- "password"  : password for the login 

"network_type" : mandatory for monitor.py : Define the network type for commands definition, supported values ("F398BT", "GEN")

"Frequency" : mandatory for monitor.py : Is the frequence when the script will launch commands

Node "Influx_Server" : mandatory for monitor.py Define the influxDB server
"Server_name"  : Name of the server,could be DNS name or IP address of the server
"Server_port"  : Port of the server "8086"
"DB_username"  : DB user name
"DB_password"  : DB password
"DB_name"      : DB name

"check_xpath" : mandatory for check_url.py : 
 ** The list of xPath to check and the expected value, define like
"xpath" : The xPath in xmo format
"expected_value" : The expected value. 
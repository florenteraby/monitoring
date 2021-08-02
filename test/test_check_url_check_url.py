import pytest

from check_url import check_upgrade_url

disc_json = {
    "network_config" : [
        {"ip":"192.168.10.11", "role": "MASTER", "name":"STUDY", "username":"root", "password":"root"}
    ],
    "network_type" : "F398BT",
    "Frequency" : "30",
    "Influx_Server" : { "Server_name"  :"ELK.home",
                        "Server_port"  : "8086",
                        "DB_username"  : "BT",
                        "DB_password"  : "BT",
                        "DB_name"      : "DEVICE_TEST"
                        }
}

def test_check_upgrade_url_1():
    assert check_upgrade_url(disc_json["network_config"]) == True

disc_json_NO_NETWORK_CONFIGURED = {
    "network_config" : [
    ],
    "network_type" : "F398BT",
    "Frequency" : "30",
    "Influx_Server" : { "Server_name"  :"ELK.home",
                        "Server_port"  : "8086",
                        "DB_username"  : "BT",
                        "DB_password"  : "BT",
                        "DB_name"      : "DEVICE_TEST"
                        }
}

def test_check_upgrade_url_2():
    assert check_upgrade_url(disc_json_NO_NETWORK_CONFIGURED["network_config"]) == False

disc_json_4_NETWORK_CONFIGURED = {
    "network_config" : [
        {"ip":"192.168.10.11", "role": "MASTER", "name":"STUDY", "username":"root", "password":"root"},
        {"ip":"192.168.10.11", "role": "MASTER", "name":"STUDY", "username":"root", "password":"root"},
        {"ip":"192.168.10.11", "role": "MASTER", "name":"STUDY", "username":"root", "password":"root"},
        {"ip":"192.168.10.11", "role": "MASTER", "name":"STUDY", "username":"root", "password":"root"}
    ],
    "network_type" : "F398BT",
    "Frequency" : "30",
    "Influx_Server" : { "Server_name"  :"ELK.home",
                        "Server_port"  : "8086",
                        "DB_username"  : "BT",
                        "DB_password"  : "BT",
                        "DB_name"      : "DEVICE_TEST"
                        }
}

def test_check_upgrade_url_3():
    assert check_upgrade_url(disc_json_4_NETWORK_CONFIGURED["network_config"]) == True

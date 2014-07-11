from .mqttclient import MQTTClientProcess
import configparser
import sys


def open_config(configfile="conf.ini"):
    config = configparser.ConfigParser()
    config.read(configfile)
    return config


def main():
    config = open_config()
    try:
        clientid = config.get('provisioning', 'device_type')+"/"+config.get('provisioning', 'serial_number')
    except:
        print("This utility requires device_type and serial_number to be configured")
        sys.exit(1)
    mqttcp = MQTTClientProcess(clientid, "sydney.matthewbrown.io", 1883)
    mqttcp.start()

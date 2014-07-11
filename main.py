from mqttclient import MQTTClientProcess
from temp import TemperatureReader
import configparser
import sys
import time


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
    temp = TemperatureReader("temperature1", mqttcp.queue)
    temp.start()
    while True:
        time.sleep(2)

if __name__ == "__main__":
    main()

from start import open_config
import paho.mqtt.client as paho
import sys
import os
import glob
import time
import click


def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp(device_file):
    lines = read_temp_raw(device_file)
    secondline = lines.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temp_string = float(temperaturedata[2:])
    temp_c = float(temp_string) / 1000.0
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    return temp_c, temp_f


def start_mqtt_client():
    config = open_config("conf.ini")
    try:
        clientid = config.get('provisioning', 'device_type')+"/"+config.get('provisioning', 'serial_number')
    except:
        print("This utility requires device_type and serial_number to be configured")
        sys.exit(1)

    try:
        host = config.get('mqttbroker', 'host')
    except:
        print("The MQTT Broker host must be configured")
        sys.exit(1)

    port = config.getint('mqttbroker', 'port', fallback=1883)

    print("Connecting to broker")
    print("Host: %s" % host)
    print("Port: %s" % port)
    mqttc = paho.Client(clientid)
    mqttc.connect(host, port=port, keepalive=60)
    print("Connected Successfully.")
    return mqttc, clientid


def check_channel(ctx, param, value):
    return value


@click.command()
@click.option("--channel", help="The channel to send data too", callback=check_channel)
def main(channel):

    clientid, mqttc = start_mqtt_client()

    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

    while True:
        c, f = read_temp(device_file)
        print(clientid, channel, c, f)
        time.sleep(1)


if __name__ == '__main__':
    main()

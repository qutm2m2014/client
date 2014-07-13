from multiprocessing import Process
from setproctitle import setproctitle
from random import randint
import time
import os
import glob


def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp(device_file):
    lines = read_temp_raw(device_file)
    temperaturedata = lines[1].split(" ")[9]
    temp_string = float(temperaturedata[2:])
    temp_c = float(temp_string) / 1000.0
    return temp_c


class TemperatureReader():

    def __init__(self, channel, queue):
        self.channel = channel
        self.queue = queue
        self.started = False
        self.process = Process(target=self.startProcess, args=(self.channel, self.queue, ))
        pass

    def start(self):
        self.process.start()
        self.started = True

    def stop(self):
        self.process.stop()
        self.started = False

    def startProcess(self, channel, queue):
        setproctitle("[M2M] Temperature Reader")
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'
        while True:
            c = read_temp(device_file)
            queue.put((channel, c))
            time.sleep(5)

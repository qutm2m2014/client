from multiprocessing import Process
from setproctitle import setproctitle
from random import randint
import time


class TemperatureReader():

    def __init__(self, channel, queue):
        self.channel = channel
        self.outQueue = queue
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
        while True:
            temp = randint(10, 15)
            queue.put((channel, temp))
            time.sleep(5)

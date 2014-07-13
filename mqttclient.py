import paho.mqtt.client as paho
from multiprocessing import Process, Queue
from setproctitle import setproctitle


class MQTTClientProcess():

    def __init__(self, clientid, broker="localhost", port=1884):
        self.queue = Queue()
        self.clientid = clientid
        self.broker = broker
        self.port = port
        self.started = False
        self.process = Process(target=self.startProcess, args=(self.queue, self.clientid, broker, port,))

    def send(self, channel, value):
        self.queue.put((channel, value))

    def start(self):
        self.process.start()
        self.started = True

    def stop(self):
        self.process.stop()
        self.started = False

    def startProcess(self, queue, clientid, host, port):
        setproctitle("MQTT Client")
        print("Connecting to broker")
        print("Host: %s" % host)
        print("Port: %s" % port)
        mqttc = paho.Client(clientid)
        mqttc.connect(host, port=port, keepalive=60)
        print("Connected Successfully.\n")
        while True:
            data = queue.get(block=True)
            print("Sending Data.\n")
            print(data[0])
            mqttc.publish("{}/{}".format(clientid, data[0]), data[1])

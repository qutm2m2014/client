import serial
import re
import subprocess
import time
from urllib.request import urlopen


def SendOS(OScom):
    """Sends commands to Raspberry OS and returns output. """
    #print "[ -- ] Sending OS command:", OScom
    commandoutput = subprocess.Popen([OScom], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    commandresult, commanderror = commandoutput.communicate()
    return commandresult, commanderror


class Modem():

    def __init__(self):
        tty, net = self.detectModem("/dev/ttyUSB3", "wwan0")
        self.ttyDevice = serial.Serial(port=tty, timeout=1)
        self.netDevice = net

    def sendAT(self, command):
        """Sends AT commands to the modem. command must be string"""
        self.ttyDevice.write((command + "\r\n").encode())
        time.sleep(2)

    def renewNetIP(self):
        SendOS("sudo dhclient -nw {0}".format(self.netDevice))  # Renew IP Address
        time.sleep(5)
        res, err = SendOS("sudo ifconfig {0}".format(self.netDevice))  # Read IP Address
        wwanip = re.search('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', str(res))
        if wwanip and not err:
            print("[ OK ] RaspberryPi {0} connected with IP address: {1}".format(self.netDevice, wwanip.group(0)))
            result = wwanip.group(0)
        else:
            print("[FAIL] RaspberryPi unable to get {0} IP address".format(self.netDevice))
            result = None
        return result

    def getModemIP():
        """
        Checks if IP address assigned on the wireless modem from cellular network
        """
        zeroIP = "0.0.0.0"
        res = urlopen('http://192.168.250.1/index.html#data')
        modemwebpage = res.read().decode('utf-8')
        modemip = re.search('(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', modemwebpage)
        if modemip:
            if modemip.group(0) != zeroIP:
                print("[ OK ] Modem connected with IP address: {0}".format(modemip.group(0)))
                result = modemip.group(0)
            else:
                print("[ -- ] No Modem IP address")
                result = None
        else:
            print("[ -- ] No Modem IP address")
            result = None
        return result

    def modemConnect(self):
        self.sendAT('AT+CFUN=1')  # Ensure Radio On
        time.sleep(10)
        self.sendAT('AT+CGDCONT=1,"IP","telstra.extranet"')  # Configure APN
        time.sleep(2)
        self.sendAT('AT!SCPROFSWOPT=1,0')
        time.sleep(2)
        self.sendAT('AT!SCPROF=1,"m2mChallenge",1,0,0,0')
        time.sleep(2)
        self.send('AT!SCACT=1,1')
        time.sleep(3)

    def start(self):
        self.modemConnect()
        time.sleep(5)
        if self.getModemIP():
            self.renewNetIP()

    @staticmethod
    def detectModem(tty, net):
        res, err = SendOS('ls %s' % (tty))
        ok = re.search(tty, str(res))
        if not ok or err:
            raise Exception()

        res, err = SendOS('sudo ifconfig %s' % (net))
        ok = re.search(net, str(res))
        if not ok or err:
            raise Exception()

        return tty, net

modem = Modem()

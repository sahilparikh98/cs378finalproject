import os
import subprocess
import sys

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
        cmd = "airodump-ng {} --essid {} -w allnet2".format(interface_name, essid)
    except KeyboardInterrupt:
		print("obtained BSSID info")

def crackWEP(bssid, essid):
    print("cracking wep")
    # open up csv file with bssid in it, split by newline and then split by
    # run besside-ng

def connectToNetwork():
    print("connecting to network")
    # close airmon stuff
    # start wireless card again
    #   

if __name__ == "__main__":
    interface = input("Please enter the interface name of your wireless network reader. You can find this by running ifconfig. It should be a wlan: ")
    monitorModeInterface = setupNetworkReader(interface)
    essid = input("Enter the ESSID (network name) of the access point you are trying to crack: ")
    getBSSIDInfo(essid, monitorModeInterface)
    
    print(bssid)
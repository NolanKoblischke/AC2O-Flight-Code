import time
import os

def elinkStatus():
    
    substring = "Link detected: yes"
    output = os.popen('sudo ethtool eth0').read()
    if substring not in output:
        print("Eth DISCONNECTED")
        # os.system("sudo reboot")
        return False
    else:
        return True

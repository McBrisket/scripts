#!/usr/bin/env python3
import os
import re
import subprocess

#check if user is in root
if os.getuid() != 0:
    print("Error: This script must be run as root")
    exit(1)
#Find externally connected interface with an IP address
ip_regex = re.compile(r"inet (?:addr:)?([\d.]+)")
interfaces = [iface for iface in os.listdir('/sys/class/net/') if not iface.startswith('lo') and not iface.startswith('wlp0s20f3')]

for interface in interfaces:
    try:
        output = subprocess.check_output(['ifconfig', interface])
        ip_match = ip_regex.search(str(output))
        if ip_match:
            external_interface = interface
            break
    except subprocess.CalledProcessError:
        print(f"Error: failed to execute ifconfig on {interface}")
        pass

#set interface to monitor mode and change the MAC address
os.system(f'sudo airmon-ng stop {interface}')
os.system(f'sudo airmon-ng start {interface}')
os.system(f'sudo ifconfig {interface} down')
os.system(f'sudo macchanger -rb {interface}')
os.system(f'sudo ifconfig {interface} up')


#run the airodump survey
os.system(f'sudo  airodump-ng --band abg {interface}mon')
if 	subprocess.CalledProcessError:
	os.system(f'sudo  airodump-ng --band abg {interface}')

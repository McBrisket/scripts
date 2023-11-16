import re
import subprocess
import time
import os

#Automatically finds the interface and uses it
def find_external_interface():
    ip_regex = re.compile(r"inet (?:addr:)?([\d.]+)")
#change the interfaces below to exclude the loopback, ethernet, and internal NIC
    interfaces = [iface for iface in os.listdir('/sys/class/net/') if not iface.startswith('lo') and not iface.startswith('wlp0s20f3')]

    for interface in interfaces:
        try:
            output = subprocess.check_output(['ifconfig', interface])
            ip_match = ip_regex.search(str(output))
            if ip_match:
                return interface
        except subprocess.CalledProcessError:
            print(f"Error: failed to execute ifconfig on {interface}")
            pass

    return None

#Define a function run_airodump that takes the network interface name (interface) as an argument. 
#This function constructs the command to run airodump-ng with the specified interface. 
#It then uses subprocess.Popen to start the process and returns the process object.
def run_airodump(interface):
    cmd = f"airodump-ng {interface}"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

# Define a function parse_airodump that takes the output of airodump-ng as input. 
#It uses a regular expression (re.compile) to extract information such as BSSID, Signal strength, and Channel from the output.
def parse_airodump(output):
    pattern = re.compile(r"([0-9A-Fa-f:]{17}).*?(-\d+).*?(\d+)")
    matches = pattern.findall(output)
    return matches

# Define the main function. Set the interface variable to the network interface you're using. 
#This may vary based on your system and hardware.
def main():
    # Find externally connected interface
    interface = find_external_interface()
    
    if interface is None:
        print("Error: No suitable interface found.")
        return
# Start a loop that runs indefinitely (while True). Inside the loop, it uses process.communicate() to get the output of airodump-ng. 
#If there's output, it parses it using the parse_airodump function and prints the relevant information. 
#This is where you would add your logic for signal strength changes and antenna orientation.
    try:
        process = run_airodump(interface)
        while True:
            output, error = process.communicate()
            if output:
                data = parse_airodump(output.decode())
                for bssid, signal, channel in data:
                    print(f"BSSID: {bssid}, Signal: {signal} dBm, Channel: {channel}")

                # Add logic for signal strength changes and antenna orientation here

            time.sleep(1)

    # Handle a KeyboardInterrupt exception (typically triggered by pressing Ctrl+C). 
    #Print a message and terminate the airodump-ng process.
    except KeyboardInterrupt:
        print("Exiting...")
        process.terminate()

if __name__ == "__main__":
    main()

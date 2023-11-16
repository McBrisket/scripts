import re
import subprocess
import time
import os

def find_external_interface():
    ip_regex = re.compile(r"inet (?:addr:)?([\d.]+)")
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

def run_airodump(interface):
    cmd = f"airodump-ng {interface}"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

def parse_airodump(output):
    pattern = re.compile(r"([0-9A-Fa-f:]{17}).*?(-\d+).*?(\d+)")
    matches = pattern.findall(output)
    return matches

def main():
    # Find externally connected interface
    interface = find_external_interface()
    
    if interface is None:
        print("Error: No suitable interface found.")
        return

    try:
        process = run_airodump(interface)
        while True:
            output, error = process.communicate()
            if output:
                data = parse_airodump(output.decode())
                for bssid, signal, channel in data:
                    print(f"BSSID: {bssid}, Signal: {signal} dBm, Channel: {channel}")

                # Add your logic for signal strength changes and antenna orientation here

            time.sleep(1)

    except KeyboardInterrupt:
        print("Exiting...")
        process.terminate()

if __name__ == "__main__":
    main()

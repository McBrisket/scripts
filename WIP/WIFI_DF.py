import re
import subprocess
import time
import os
import serial

# Function to find the externally connected interface with an IP address
def find_external_interface():
    ip_regex = re.compile(r"inet (?:addr:)?([\d.]+)")
    
    # Exclude loopback, ethernet, and internal NIC interfaces
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

# Function to run airodump-ng on the specified interface
def run_airodump(interface):
    cmd = f"airodump-ng {interface}"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

# Function to parse the output of airodump-ng and extract relevant information
def parse_airodump(output):
    pattern = re.compile(r"([0-9A-Fa-f:]{17}).*?(-\d+).*?(\d+)")
    matches = pattern.findall(output)
    return matches

# Function to initialize the GPS lock, wait until a good lock is obtained
def initialize_gps_lock():
    print("Initializing GPS lock. Please wait...")
    while True:
        latitude, longitude = get_gps_data()
        if latitude is not None and longitude is not None:
            print(f"GPS Lock obtained - Latitude: {latitude}, Longitude: {longitude}")
            return

# Function to obtain GPS data from a serial port
def get_gps_data(serial_port='/dev/ttyUSB0'):
    try:
        with serial.Serial(serial_port, 9600, timeout=1) as ser:
            line = ser.readline().decode('utf-8').strip()
            parts = line.split(',')
            if parts[0] == '$GPGGA' and len(parts) >= 10:
                latitude = float(parts[2][:2]) + float(parts[2][2:]) / 60.0
                longitude = float(parts[4][:3]) + float(parts[4][3:]) / 60.0
                return latitude, longitude
    except serial.SerialException as e:
        print(f"Error reading GPS data: {e}")
    return None, None

# Main function
def main():
    # Find externally connected interface
    interface = find_external_interface()
    
    if interface is None:
        print("Error: No suitable interface found.")
        return

    # Initialize GPS lock before starting airodump-ng
    initialize_gps_lock()

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

    except KeyboardInterrupt:
        print("Exiting...")
        process.terminate()

if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import filedialog
from scapy.all import rdpcap

def handle_files():
    # Ask the user to select pcap files
    pcap_files = filedialog.askopenfilenames(title="Select pcap files", filetypes=(("PCAP files", "*.pcap"),))

    # Print the selected files
    print("Selected files:")
    for i, pcap_file in enumerate(pcap_files):
        print(f"File {i+1}: {pcap_file}")

    # Create a list of sets to store the MAC addresses
    mac_sets = [set() for _ in range(len(pcap_files))]

    # Open each pcap file and extract the MAC addresses
    for i, pcap_file in enumerate(pcap_files):
        packets = rdpcap(pcap_file)
        for packet in packets:
            if packet.haslayer('Dot11') and packet.addr2 is not None:
                mac_address = packet.addr2.upper()
                mac_sets[i].add(mac_address)

    # Find the common MAC addresses in all sets
    common_macs = set.union(*mac_sets)

    # Count how many times each MAC address appears in the sets and which files it appeared in
    mac_counts = {}
    for mac in common_macs:
        count = 0
        file_set = set()
        for i, mac_set in enumerate(mac_sets):
            if mac in mac_set:
                count += 1
                file_set.add(f"PCAP file {i+1}")
        if count >= 2:
            mac_counts[mac] = {"count": count, "files": file_set}

    # Sort the MAC addresses by descending correlation count
    sorted_macs = sorted(mac_counts.items(), key=lambda x: x[1]['count'], reverse=True)

    # Print the common MAC addresses that appear at least twice and which files they appeared in
    print("\nCommon MAC addresses:")
    for mac, count_files in sorted_macs:
        print(f"{mac}: correlated {count_files['count']} times in {', '.join(count_files['files'])}")

# Create the GUI window
window = tk.Tk()

# Create a button to handle files
button = tk.Button(window, text="Select PCAP files", command=handle_files)
button.pack()

# Run the GUI event loop
window.mainloop()

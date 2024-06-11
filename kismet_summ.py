import os
import pandas as pd
from collections import Counter
from lxml import etree
from tkinter import Tk, filedialog

def parse_kismet_file(filepath):
    with open(filepath, 'r') as file:
        tree = etree.parse(file)
        root = tree.getroot()
        
        # Initialize data containers
        num_devices = 0
        ssids = []
        bssids = []
        channels = set()
        
        for device in root.findall('device'):
            num_devices += 1
            ssid = device.find('SSID')
            if ssid is not None and ssid.text:
                ssids.append(ssid.text)
            bssid = device.find('BSSID')
            if bssid is not None and bssid.text:
                bssids.append(bssid.text)
            channel = device.find('channel')
            if channel is not None and channel.text:
                channels.add(channel.text)
        
        # Determine the most common SSID and BSSID
        most_common_ssid = Counter(ssids).most_common(1)
        most_common_bssid = Counter(bssids).most_common(1)
        
        return {
            'num_devices': num_devices,
            'unique_ssids': len(set(ssids)),
            'unique_channels': len(channels),
            'most_common_ssid': most_common_ssid[0][0] if most_common_ssid else None,
            'most_common_bssid': most_common_bssid[0][0] if most_common_bssid else None
        }

def summarize_kismet_logs(filepaths):
    summary = []
    
    for filepath in filepaths:
        file_summary = parse_kismet_file(filepath)
        file_summary['file'] = os.path.basename(filepath)
        summary.append(file_summary)
    
    # Create a DataFrame for better readability
    summary_df = pd.DataFrame(summary)
    
    return summary_df

def select_files():
    # Open file dialog to select multiple Kismet files
    root = Tk()
    root.withdraw()  # Hide the root window
    filepaths = filedialog.askopenfilenames(title="Select Kismet Files", filetypes=[("Kismet Files", "*.kismet")])
    return filepaths

# Main script
filepaths = select_files()
if filepaths:
    summary_df = summarize_kismet_logs(filepaths)
    print(summary_df)
else:
    print("No files selected.")


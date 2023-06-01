import csv
import tkinter as tk
from tkinter import filedialog
import os

def handle_files():
    # Ask the user to select CSV files
    csv_files = filedialog.askopenfilenames(title="Select CSV files", filetypes=(("CSV files", "*.csv"),))

    # Print the selected files
    print("Selected files:")
    for i, csv_file in enumerate(csv_files):
        print(f"File {i+1}: {csv_file}")

    # Create a list of sets to store the MAC addresses
    mac_sets = [set() for _ in range(len(csv_files))]

    # Open each CSV file and extract the MAC addresses
    for i, csv_file in enumerate(csv_files):
        _, file_extension = os.path.splitext(csv_file)

        with open(csv_file, "r") as f:
            reader = csv.reader(f)

            if file_extension == ".kismet.csv":
                header_row = next(reader)  # Get the header row for .kismet.csv files
                bssid_index = 3 if "BSSID" in header_row else -1  # Assuming BSSID is in the fourth column
            else:
                bssid_index = 0  # Assuming BSSID is in the first column for regular .csv files

            for row in reader:
                if bssid_index >= 0 and len(row) > bssid_index:
                    mac_address = row[bssid_index].replace(",", "").upper()
                    if mac_address != "BSSID" and mac_address != "STATION MAC":
                        mac_sets[i].add(mac_address)

    # Find the common MAC addresses in at least two sets
    common_macs = set.union(*mac_sets)

    # Count how many times each MAC address appears in the sets and which files it appeared in
    mac_counts = {}
    for mac in common_macs:
        count = 0
        file_set = set()
        for i, mac_set in enumerate(mac_sets):
            if mac in mac_set:
                count += 1
                file_set.add(f"CSV file {i+1}")
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
button = tk.Button(window, text="Select CSV files", command=handle_files)
button.pack()

# Run the GUI event loop
window.mainloop()

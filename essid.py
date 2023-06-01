import csv
import tkinter as tk
from tkinter import filedialog

def handle_files():
    # Ask the user to select CSV files
    csv_files = filedialog.askopenfilenames(title="Select CSV files", filetypes=(("CSV files", "*.csv"),))

    # Print the selected files
    print("Selected files:")
    for i, csv_file in enumerate(csv_files):
        print(f"File {i+1}: {csv_file}")

    # Create a list of sets to store the ESSIDs
    essid_sets = [set() for _ in range(len(csv_files))]

    # Open each CSV file and extract the ESSIDs
    for i, csv_file in enumerate(csv_files):
        with open(csv_file, "r") as f:
            reader = csv.reader(f)
            next(reader)  # skip the first row
            for _ in range(1):  # skip the second row
                next(reader)
            for row in reader:
                if len(row) >= 14:  # Check if the row has at least 14 columns
                    essid = row[13].replace(",", "").upper()  # Assuming ESSIDs are in the 14th column
                    essid_sets[i].add(essid)

    # Find the common ESSIDs in all sets
    common_essids = set.union(*essid_sets)

    # Count how many times each ESSID appears in the sets and which files it appeared in
    essid_counts = {}
    for essid in common_essids:
        count = 0
        file_set = set()
        for i, essid_set in enumerate(essid_sets):
            if essid in essid_set:
                count += 1
                file_set.add(f"CSV file {i+1}")
        if count >= 2:
            essid_counts[essid] = {"count": count, "files": file_set}

    # Sort the ESSIDs by descending correlation count
    sorted_essids = sorted(essid_counts.items(), key=lambda x: x[1]['count'], reverse=True)

    # Print the common ESSIDs that appear at least twice and which files they appeared in
    print("\nCommon ESSIDs:")
    for essid, count_files in sorted_essids:
        print(f"{essid}: correlated {count_files['count']} times in {', '.join(count_files['files'])}")

# Create the GUI window
window = tk.Tk()

# Create a button to handle files
button = tk.Button(window, text="Select CSV files", command=handle_files)
button.pack()

# Run the GUI event loop
window.mainloop()

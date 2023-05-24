import csv

# Ask the user for the number of CSV files to use
num_csv_files = int(input("Enter the number of CSV files: "))

# Create a list of sets to store the MAC addresses
mac_sets = [set() for _ in range(num_csv_files)]

# Open each CSV file and extract the MAC addresses
for i in range(num_csv_files):
    csv_file = input(f"Enter the name of CSV file {i+1}: ")
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f, fieldnames=['BSSID'])
        next(reader)  # skip the first row
        for row in reader:
            mac_address = row["BSSID"].replace(",", "").upper()
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
            file_set.add(f"CSV file {i+1}")
    if count >= 2:
        mac_counts[mac] = {"count": count, "files": file_set}

# Print the common MAC addresses that appear at least twice and which files they appeared in
print("Common MAC addresses:")
for mac, count_files in mac_counts.items():
    print(f"{mac}: correlated {count_files['count']} times in {', '.join(count_files['files'])}")

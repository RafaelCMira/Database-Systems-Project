import csv
import sys

def convert_to_csv(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    initialTs = 0 # In seconds

    data = []
    for line in lines:
        if line.startswith('Hammerdb') or line.startswith('+-'):
            continue
        parts = line.split()
        counter = parts[0]
        timestamp = initialTs
        initialTs = initialTs + 5
        data.append([counter, timestamp])

    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['TPM', 'time'])
        csv_writer.writerows(data)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_to_csv(input_file, output_file)
    print("Conversion completed.")
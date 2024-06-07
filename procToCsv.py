import os
import tempfile
import argparse
import csv
import re

def convert_to_csv(input_file, output_file):
    summary_started = False
    summary_ended = False

    with open(input_file, 'r') as f, open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['PROC', 'CALLS', 'MIN', 'AVG', 'MAX', 'TOTAL', 'P99', 'P95', 'P50', 'SD', 'RATIO']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for line in f:
            if 'SUMMARY OF' in line:  # Start of summary section
                summary_started = True
                continue
            if summary_started:
                if 'SUMMARY' in line and not summary_ended:  # End of summary section
                    summary_ended = True
                    break
                if line.startswith('>>>>> PROC:'):
                    proc = line.split(':')[1].strip()
                    data = next(f).strip().split('\t')
                    row = {'PROC': proc}
                    for item in data:
                        key, value = item.split(':')
                        row[key] = value.strip()
                    # Read the next line and extract the data for the remaining columns
                    data = next(f).strip().split('\t')
                    for item in data:
                        key, value = item.split(':')
                        row[key] = value.strip()
                    writer.writerow(row)

def split_and_convert(input_file):
    with open(input_file, 'r') as f:
        temp_file = None
        file_count = 0
        for line in f:
            if 'PostgreSQL Hammerdb Time Profile Report' in line:
                # If a temporary file is already open, close it and convert to CSV
                if temp_file is not None:
                    temp_file.close()
                    with open(temp_file.name, 'r') as temp_file_read:
                        contents = temp_file_read.read()
                    output_file = re.search(r'SUMMARY OF (\d+) ACTIVE', contents)
                    if output_file is not None:
                        output_file = output_file.group(1)  # Extract the number of virtual users
                    convert_to_csv(temp_file.name, f"{output_file}PROC.csv")
                    os.remove(temp_file.name)  # Delete the temporary file
                # Start a new temporary file
                temp_file = tempfile.NamedTemporaryFile(delete=False)
                file_count += 1
            temp_file.write(line.encode())  # Write the line to the temporary file
        # Convert the last section to CSV
        if temp_file is not None:
            temp_file.close()
            with open(temp_file.name, 'r') as temp_file_read:
                contents = temp_file_read.read()
            output_file = re.search(r'SUMMARY OF (\d+) ACTIVE', contents)
            if output_file is not None:
                output_file = output_file.group(1)  # Extract the number of virtual users
            convert_to_csv(temp_file.name, f"{output_file}PROC.csv")
            os.remove(temp_file.name)  # Delete the temporary file

def main():
    parser = argparse.ArgumentParser(description='Convert log file to CSV.')
    parser.add_argument('input_file', help='The log file to convert')
    args = parser.parse_args()

    split_and_convert(args.input_file)

if __name__ == "__main__":
    main()
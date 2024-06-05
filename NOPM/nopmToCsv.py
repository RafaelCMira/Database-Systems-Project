import argparse
import csv
import re

def convert_to_csv(input_file, output_file):
    with open(input_file, 'r') as f, open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['PROC', 'CALLS', 'MIN', 'AVG', 'MAX', 'TOTAL', 'P99', 'P95', 'P50', 'SD', 'RATIO']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for line in f:
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

def main():
    parser = argparse.ArgumentParser(description='Convert log file to CSV.')
    parser.add_argument('input_file', help='The log file to convert')
    parser.add_argument('output_file', help='The output CSV file')
    args = parser.parse_args()

    convert_to_csv(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
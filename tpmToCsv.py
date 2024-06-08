import csv
import sys

EXPERIMENT_BREAKER = 100

def convert_to_csv(input_file, experiment_numbers):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    experiment_data = []
    current_experiment = []
    initialTs = 0  # In seconds

    for line in lines:
        if line.startswith('Hammerdb') or line.startswith('+-') or not line.strip():
            continue
        parts = line.split()

        # Check if the first part is a digit and if parts has enough elements
        if len(parts) < 2 or not parts[0].isdigit():
            continue

        counter = int(parts[0])

        # Check for separators indicating the end of an experiment
        if counter <= EXPERIMENT_BREAKER and current_experiment:
            if len(current_experiment) > 1:  # Skip the separator values at the start of each experiment
                experiment_data.append(current_experiment)
            current_experiment = []
            initialTs = 0
            continue

        timestamp = initialTs
        initialTs += 10
        current_experiment.append([counter, timestamp])

    # Append the last experiment if it wasn't added
    if current_experiment and len(current_experiment) > 1:
        experiment_data.append(current_experiment)

    for i, experiment in enumerate(experiment_data):
        if i >= len(experiment_numbers):
            break

        output_file = f'{experiment_numbers[i]}TPM.csv'
        with open(output_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['TPM', 'time'])
            # Skip initial separator values
            if len(experiment) > 2 and experiment[0][0] <= 10 and experiment[1][0] <= 10:
                csv_writer.writerows(experiment[2:])
            else:
                csv_writer.writerows(experiment)
        print(f"Conversion for experiment {experiment_numbers[i]} completed: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py input_file experiment_number1 experiment_number2 ...")
        sys.exit(1)

    input_file = sys.argv[1]
    experiment_numbers = sys.argv[2:]
    convert_to_csv(input_file, experiment_numbers)

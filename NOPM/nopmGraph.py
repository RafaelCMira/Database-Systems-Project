import pandas as pd
import matplotlib.pyplot as plt
import argparse

def plot_graph(file, proc):
    data = pd.read_csv(file)

    # Filter the data for the specified PROC
    data = data[data['PROC'] == proc]

    # Specify the columns you want to display
    columns_to_display = ['P50', 'P95', 'P99', 'AVG']
    data = data[columns_to_display]

    # Remove units and convert to numbers for columns of object type
    for column in data.select_dtypes(include=[object]).columns:
        data[column] = data[column].str.replace('ms', '').str.replace('%', '').astype(float)

    # Convert the data to a single row
    data = data.squeeze()

    # Specify the colors for each bar
    colors = ['#5470c6' , '#91cc75', '#fac858', '#ee6666']

    # Create a bar graph
    plt.figure(figsize=(10, 6))
    bars = plt.bar(data.index, data.values, color=colors, edgecolor='black', linewidth=1)

    # Add the values above the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom', ha='center')  # ha: horizontal alignment

    plt.title(proc)
    plt.xlabel('Metric')
    plt.ylabel('Milliseconds')

    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Plot graph for a specific process from a CSV file.')
    parser.add_argument('input_file', help='The input CSV file')
    parser.add_argument('proc', help='The process to plot')
    args = parser.parse_args()

    plot_graph(args.input_file, args.proc)

if __name__ == "__main__":
    main()
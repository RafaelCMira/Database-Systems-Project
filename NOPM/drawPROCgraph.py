import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np


# def plot_graph(file, procs, bar_width=0.1, space_within_proc=0.1, space_between_procs=0.5):
#     data = pd.read_csv(file)
#
#     plt.figure(figsize=(10, 6))
#
#     # Specify the columns you want to display
#     columns_to_display = ['P50', 'P95', 'P99', 'AVG']
#
#     for i, proc in enumerate(procs):
#         # Filter the data for the specified PROC
#         proc_data = data[data['PROC'] == proc]
#         proc_data = proc_data[columns_to_display]
#
#         # Remove units and convert to numbers for columns of object type
#         for column in proc_data.select_dtypes(include=[object]).columns:
#             proc_data[column] = proc_data[column].str.replace('ms', '').str.replace('%', '').astype(float)
#
#         # Convert the data to a single row
#         proc_data = proc_data.squeeze()
#
#         # Specify the colors for each bar
#         colors = ['#5470c6' , '#91cc75', '#fac858', '#ee6666']
#
#         # Create a bar graph
#         for j, metric in enumerate(columns_to_display):
#             x = j * (bar_width + space_within_proc) + i * (len(columns_to_display) * (bar_width + space_within_proc) + space_between_procs)
#             plt.bar(x, proc_data[metric], color=colors[j], edgecolor='black', linewidth=1, width=bar_width)
#
#     plt.title('Multiple PROCs')
#     plt.xlabel('Metric')
#     plt.ylabel('Milliseconds')
#     plt.xticks([i * (len(columns_to_display) * (bar_width + space_within_proc) + space_between_procs) + (len(columns_to_display) * (bar_width + space_within_proc) / 2) - bar_width/2 for i in range(len(procs))],
#                procs)  # set the x-ticks to be the PROCs
#
#     plt.show()
#
# def main():
#     parser = argparse.ArgumentParser(description='Plot graph for specific processes from a CSV file.')
#     parser.add_argument('input_file', help='The input CSV file')
#     parser.add_argument('procs', nargs='+', help='The processes to plot')
#     parser.add_argument('--bar_width', type=float, default=0.05, help='The width of the bars')
#     parser.add_argument('--space_within_proc', type=float, default=0.01, help='The space within PROCs')
#     parser.add_argument('--space_between_procs', type=float, default=0.2, help='The space between PROCs')
#     args = parser.parse_args()  # parse the arguments and assign to args
#     plot_graph(args.input_file, args.procs, args.bar_width, args.space_within_proc, args.space_between_procs)
#
# if __name__ == "__main__":
#     main()


def plot_graph(file, procs, bar_width=0.1, space_within_proc=0.1, space_between_procs=0.5):
    data = pd.read_csv(file)

    plt.figure(figsize=(12, 6))

    # Specify the columns you want to display
    columns_to_display = ['P50', 'P95', 'P99', 'AVG']

    for i, proc in enumerate(procs):
        # Filter the data for the specified PROC
        proc_data = data[data['PROC'] == proc]
        proc_data = proc_data[columns_to_display]

        # Remove units and convert to numbers for columns of object type
        for column in proc_data.select_dtypes(include=[object]).columns:
            proc_data[column] = proc_data[column].str.replace('ms', '').str.replace('%', '').astype(float)

        # Convert the data to a single row
        proc_data = proc_data.squeeze()

        # Specify the colors for each bar
        colors = ['#5470c6' , '#91cc75', '#fac858', '#ee6666']

        # Create a bar graph
        for j, metric in enumerate(columns_to_display):
            x = j * (bar_width + space_within_proc) + i * (len(columns_to_display) * (bar_width + space_within_proc) + space_between_procs)
            bar = plt.bar(x, proc_data[metric], color=colors[j], edgecolor='black', linewidth=1, width=bar_width)
            plt.text(bar[0].get_x() + bar[0].get_width() / 2, bar[0].get_height(), str(proc_data[metric]), ha='center', va='bottom')

    plt.title('Multiple PROCs')
    plt.xlabel('Metric')
    plt.ylabel('Milliseconds')
    plt.xticks([i * (len(columns_to_display) * (bar_width + space_within_proc) + space_between_procs) + (len(columns_to_display) * (bar_width + space_within_proc) / 2) - bar_width/2 for i in range(len(procs))],
               procs)  # set the x-ticks to be the PROCs

    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Plot graph for specific processes from a CSV file.')
    parser.add_argument('input_file', help='The input CSV file')
    parser.add_argument('procs', nargs='+', help='The processes to plot')
    parser.add_argument('--bar_width', type=float, default=0.5, help='The width of the bars')
    parser.add_argument('--space_within_proc', type=float, default=0.1, help='The space within PROCs')
    parser.add_argument('--space_between_procs', type=float, default=0.2, help='The space between PROCs')
    args = parser.parse_args()  # parse the arguments and assign to args
    plot_graph(args.input_file, args.procs, args.bar_width, args.space_within_proc, args.space_between_procs)

if __name__ == "__main__":
    main()
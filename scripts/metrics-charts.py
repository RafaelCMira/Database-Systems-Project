#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt 
import sys
from os import path

class StatsHeader:
    TIME_STAMP = 'Timestamp'
    CPU = 'CPU%'
    MEM = 'MemUsage'
    NET = 'NetIO',
    IO  = 'BlockIO'
    VU  = 'VirtuaUsers'

hd = StatsHeader

USED_VIRTUAL_USERS = [8, 16, 32, 64, 100]

def get_vu_labels(ax) -> list[str]:
    return  [
        label.strip('() ').split()[1] for label in ax.get_legend_handles_labels()[1]
    ]

def plot_mem( frame : pd.DataFrame, out_file : str):
    groups = frame.groupby([hd.VU, hd.TIME_STAMP])[hd.MEM].mean().to_frame()
    groups.reset_index(level=(hd.VU,), inplace=True)

    pivot_data = groups.pivot(columns=hd.VU)

    plt.figure()
    ax = pivot_data.plot(
        kind = 'line',
    )

    plt.legend(title='Virtual Users Number', labels=get_vu_labels(ax))
    plt.xlabel("time minutes")
    plt.ylabel("Memory usage (GibaBytes)")
    plt.title("Amount of memory used by Database")

    plt.savefig(out_file)
    print(f"generated '{out_file}'")



def plot_cpu( frame : pd.DataFrame, out_file : str ):
    groups = frame.groupby([hd.VU, hd.TIME_STAMP])[hd.CPU].mean().to_frame()

    groups.reset_index(level=(hd.VU,), inplace=True)
    pivot_data = groups.pivot(columns=hd.VU)

    plt.figure()
    ax = pivot_data.plot(
        kind = 'line',
    )

    plt.legend(title='Virtual Users Number', labels=get_vu_labels(ax))
    plt.xlabel("time minutes")
    plt.ylabel("CPU usage (%)")
    plt.title("CPU Usage during the experiment")

    plt.savefig(out_file)
    print(f"generated '{out_file}'")


def plot_io(frame : pd.DataFrame, out_file : str):
    groups = frame.groupby([hd.VU, hd.TIME_STAMP])[hd.IO].agg('sum').to_frame()

    groups.reset_index(level=(hd.VU,), inplace=True)

    pivot_data = groups.pivot(columns=hd.VU).fillna(0)

    plt.figure()
    ax = pivot_data.plot(
        kind = 'line',
    )

    plt.legend(title='Virtual Users Number', labels=get_vu_labels(ax))
    plt.xlabel("time minutes")
    plt.ylabel("Total memory transfered on I/O operations (GigaBytes)")
    plt.title("I/O Memory Transfer to Disk")

    plt.savefig(out_file)
    print(f"generated '{out_file}'")

def main(args : list[str]):

    if len(args) < 2:
        print('Error: Missing arguments!', file=sys.stderr)
        print(f'usage: {args[0]} <dir-name>', file=sys.stderr)
        sys.exit(1)

    dirname  = args[1]
    print(f"Reading files from '{dirname}'")
    data = pd.read_csv(
        path.join(dirname, 'resource-metrics.csv')
    )

    plot_mem(  data, path.join(dirname, 'mem-usage.pdf'))
    plot_io(   data, path.join(dirname, 'io-transfer.pdf'))
    plot_cpu(  data, path.join(dirname, 'cpu-usage.pdf'))

if __name__ == '__main__':
    main(sys.argv)

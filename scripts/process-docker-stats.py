#!/usr/bin/env python3

import re
import sys
import pandas as pd
from datetime import datetime
from os import path

from dateutil import tz

EXPERIMENT_BREAKER = 300
DATETIME_FMT = '%a %b %d %H:%M:%S %Z %Y'
PATTERN = re.compile(r"(\d+) PostgreSQL tpm @ (.+)")

USED_VIRTUAL_USERS = [8, 16, 32, 64, 100]

class StatsHeader:
    TIME_STAMP = 'Timestamp'
    CPU = 'CPU%'
    MEM = 'MemUsage'
    NET = 'NetIO',
    IO  = 'BlockIO'
    VU  = 'VirtuaUsers'

hd = StatsHeader
def read_file( filename : str ) -> str:
    with open(filename) as file:
        return file.read()

def utc_to_local_time( time : datetime ) -> datetime:
    # FIXME: someday
    from_zone = tz.tzutc()
    to_zone   = tz.tzlocal()
    utc       = time.replace(tzinfo=from_zone)
    return utc.astimezone(to_zone)
n = 0

def utc_str_to_unix_time( time : str ): #-> int:
    global n
    utc   = datetime.strptime(time, DATETIME_FMT)
    local = utc_to_local_time(utc)
    print(time, end= ',' if n % 2 == 0 else '\n')
    n += 1

    return int( local.timestamp() )

def load_intervals(filename : str ) -> list[tuple[int, int]]:
    data = read_file(filename)

    intervals = []
    rows  = re.findall(PATTERN, data)

    start = utc_str_to_unix_time(rows[0][1])

    for i,(tpm, date) in enumerate(rows[1:]):
        tpm_val = int(tpm)
        if start == None and tpm_val >= EXPERIMENT_BREAKER:
            start = utc_str_to_unix_time(date)
        elif start != None and tpm_val < EXPERIMENT_BREAKER:
            date = rows[i][1] # because of + 1 from above
            intervals.append(
                (start, utc_str_to_unix_time(date))
            )
            start = None

    return intervals

def str_to_mega_bytes( value : str ) -> float:
    i = 0
    while value[i].isdigit() or value[i] == '.':
        i += 1

    numeric_value = float(value[:i])
    unit = value[i:]

    assert unit != ''

    if unit in ['GB', 'GiB']:
        base = 2 ** 30
    elif unit in ['MB', 'MiB']:
        base = 2 ** 20
    elif unit in ['kB', 'KiB']:
        base = 2 ** 10
    elif unit == 'B':
        base = 1
    else:
        assert False, f'Something is clearly wrong {value}'

    return base * numeric_value / 2 ** 20


def convert_io( value : str ) -> float:
    [input, output] = value.split('/')
    return str_to_mega_bytes(input.strip()) + str_to_mega_bytes(output.strip())

def process_stats_data( stats : pd.DataFrame, intervals : list[tuple[int, int]]) -> pd.DataFrame:
    results = []
    for vu,(start, end) in zip(USED_VIRTUAL_USERS, intervals):
        data = stats[
            stats[hd.TIME_STAMP].between(start, end)
        ].copy()

        assert len(data) > 0, f'for {vu} ({start}, {end}) ; data = {str(stats)}'
        assert type(data) == pd.DataFrame

        data[hd.VU] = vu
        data[hd.TIME_STAMP] = round(
            (data[hd.TIME_STAMP] - start) / 60, 0
        ).astype(int)
        data[hd.MEM] -= data[hd.MEM].iloc[0]

        results.append(
            data
        )

    return pd.concat( results )


def read_stats_file(filename : str) -> pd.DataFrame:
    data = pd.read_csv(filename)
    data[hd.VU]  = 0
    io_per_second  = data[hd.IO].apply(convert_io).diff() / data[hd.TIME_STAMP].diff()
    mem_mega_bytes = data[hd.MEM].apply(
        lambda value : str_to_mega_bytes(
            value.split('/', maxsplit=1)[0].strip()
        )
    ) 

    data[hd.IO]  =  io_per_second.round(2)
    data[hd.MEM] = mem_mega_bytes.round(2)

    data[hd.CPU] = data[hd.CPU].apply(
        lambda value : value[:-1]
    )

    return data

def main(args: list[str]):
    if len(args) < 2:
        print('Error: Missing arguments!', file=sys.stderr)
        print(f'usage: {args[0]} <dir-name>', file=sys.stderr)
        sys.exit(1)

    dirname = args[1]
    print(f"Handling files from '{dirname}'")

    tpm_count_file  = path.join(dirname, 'tpm/hdbtcount.log')
    status_log_file = path.join(dirname, 'docker-stats.log')

    print(tpm_count_file)
    intervals = load_intervals(tpm_count_file)
    assert len(intervals) == len(USED_VIRTUAL_USERS) or len(intervals) == 2, len(intervals)
    stats  = read_stats_file(status_log_file)
    result = process_stats_data(stats, intervals)

    output_file = path.join(dirname, 'resource-metrics.csv')
    result.to_csv(
        output_file, index=False, float_format='%.2f'
    )

    print(f"Saving results to '{output_file}'")

if __name__ == '__main__':
    main(sys.argv)

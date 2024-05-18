#!/usr/bin/env python3

import re
import pandas as pd
import matplotlib.pyplot as plt

USER_SPLIT = '+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+'
FILE_NAME  = "hdbxtprofile.log"

USER_NR    = re.compile(r'VIRTUAL USER (\d+)')
STAT_SPLIT = '>>>>> PROC:'
METRICS    = re.compile(r'(\w+?): ((\d|\.)+)')



def conver_file(src_file : str, output_file : str):
    with open(src_file, 'r') as f:
        text = f.read()

    # -2 because the last one is a summary c:
    users_data = text.split(USER_SPLIT)[1:-2]

    # (user_nr, stat_name, metric_name, metric_value)
    result = []
    for data in users_data:
        res = USER_NR.search(data)
        assert res != None, 'BUG: Getting user number : ' + data
        user_nr = res.group(1)
        # print(f'user-nr: {user_nr} ...')
        stats = data.split(STAT_SPLIT)[1:]
        for st in stats:
            lines = st.split('\n')
            stat_name = lines[0].strip()
            # print('stat-name:', stat_name)

            for line in lines[1:]:
                for m in METRICS.finditer(line):
                    # print(m.group(1), ':', m.group(2))
                    metric_name = m.group(1)
                    metric_value = m.group(2)
                    result.append([
                        user_nr, stat_name, metric_name, metric_value
                    ])

    frame = pd.DataFrame(result, columns=['user-nr', 'proc-name', 'metric-name', 'metric-value'])
    frame.set_index('user-nr', inplace=True)
    frame.to_csv(output_file)


def main():
    pass
    # frame = pd.read_csv('file.csv')
    #
    # rows = frame[ 
    #     (frame['user-nr'] == 2) & (frame['proc-name'] == 'NEWORD') 
    #              & (frame['metric-name'] != 'TOTAL')
    # ].copy()
    #
    #
    # rows.drop(columns=['user-nr', 'proc-name'], inplace=True)
    # rows.set_index('metric-name', inplace=True)
    # plt.show()

if __name__ == '__main__':
    main()

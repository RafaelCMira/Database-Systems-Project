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

    # Data
    data = {
        'proc-name': 'NEWORD',
        'CALLS': '116915',
        'MIN': '1.232',
        'AVG': '3.828',
        'MAX': '446.229',
        'TOTAL': '447559.596',
        'P99': '12.260',
        'P95': '5.590',
        'P50': '3.210',
        'SD': '59951.357',
        'RATIO': '57.204'
    }

# Plot
    plt.figure(figsize=(10, 6))
    keys = list(data.keys())[1:]  # Exclude 'proc-name'
    values = [float(value) for key, value in data.items() if key != 'proc-name']
    bars = plt.bar(keys, values)
    plt.title(data['proc-name'])
    plt.xlabel('Metrics')
    plt.ylabel('Value (ms)')
    plt.xticks(rotation=0)  # Rotate x-axis labels to be horizontal

    # Annotate bars with their values
    for bar in bars:
        yval = bar.get_height()
        xval = bar.get_x() + bar.get_width() / 2
        plt.text(xval, yval, round(yval, 2), ha='center', va='bottom')

    # Adjust y-axis limits
    plt.ylim(0, max(values) * 1.1)  # Extend the limit by 10% for better visibility

    plt.show()

if __name__ == '__main__':
    main()

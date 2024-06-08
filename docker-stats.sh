#!/usr/bin/env bash

if [ $# -lt 1 ] ; then
    echo "usage: $0 <output-file>"
    exit 1
fi

output_file=$1
echo "Will save output in '$output_file'."
# Write header
echo "Timestamp,CPU%,MemUsage,NetIO,BlockIO,PIDs" > $output_file

while true; do
    timestamp=$(date '+%s')
    line=$(docker stats --no-stream --format \
            "{{.CPUPerc}},{{.MemUsage}},{{.NetIO}},{{.BlockIO}},{{.PIDs}}")
    echo "$timestamp;$line" >> $output_file
done

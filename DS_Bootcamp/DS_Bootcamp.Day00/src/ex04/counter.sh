#!/bin/sh

if [ ! -f ../ex03/hh_positions.csv ]; then
  echo "Файл hh_positions.csv не найден."
  exit 1
fi

input_file="../ex03/hh_positions.csv"
output_file="hh_uniq_positions.csv"

{
    echo '"name","count"' 
    tail -n +2 "$input_file" | cut -d, -f3 | sort | uniq -c | sort -nr | {
    while read -r count name; do
        if [ "${name}" != "-" ]; then
            echo "$name,$count"
        fi
    done
} } > "$output_file"

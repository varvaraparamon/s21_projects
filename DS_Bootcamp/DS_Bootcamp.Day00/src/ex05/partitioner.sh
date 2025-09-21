#!/bin/sh

if [ ! -f ../ex03/hh_positions.csv ]; then
  echo "Файл hh_positions.csv не найден."
  exit 1
fi

input_file="../ex03/hh_positions.csv"

header=$(head -n 1 "$input_file")

tail -n +2 "$input_file" | while IFS=, read -r id created_at name has_test alternate_url; do
    date=$(echo "$created_at" | cut -d'T' -f1)

    output_file="hh_positions_$date.csv"

    if [ ! -f "$output_file" ]; then
        echo "$header" > "$output_file"
    fi

    echo "$id,$created_at,$name,$has_test,$alternate_url" >> "$output_file"
done

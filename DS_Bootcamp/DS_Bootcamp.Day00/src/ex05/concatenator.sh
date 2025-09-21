#!/bin/sh

output_file="hh_concatenated_positions.csv"

echo '"id","created_at","name","has_test","alternate_url"' > "$output_file"

for file in hh_positions_*.csv; do
    tail -n +2 "$file" >> "$output_file"
done

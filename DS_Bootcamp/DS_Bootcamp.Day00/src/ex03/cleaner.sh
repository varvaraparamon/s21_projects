#!/bin/sh

if [ ! -f ../ex02/hh_sorted.csv ]; then
  echo "Файл hh_sorted.csv не найден."
  exit 1
fi


clean_position_name() {
    local name="$1"
    local cleaned_name="-"

    if [ "${name#*Junior}" != "$name" ]; then
        cleaned_name="Junior"
    fi
    if [ "${name#*Middle}" != "$name" ]; then
        if [ "$cleaned_name" = "-" ]; then
            cleaned_name="Middle"
        else
            cleaned_name="$cleaned_name/Middle"
        fi
    fi
    if [ "${name#*Senior}" != "$name" ]; then
        if [ "$cleaned_name" = "-" ]; then
            cleaned_name="Senior"
        else
            cleaned_name="$cleaned_name/Senior"
        fi
    fi

    echo "$cleaned_name"
}

{
    head -n 1 "../ex02/hh_sorted.csv"

    tail -n +2 "../ex02/hh_sorted.csv" | while IFS=, read -r id created_at name has_test alternate_url; do
        cleaned_name=$(clean_position_name "$name")

        echo "$id,$created_at,$cleaned_name,$has_test,$alternate_url"

    done
} > "hh_positions.csv"



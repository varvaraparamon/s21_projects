#!/bin/sh

if [ ! -f ../ex00/hh.json ]; then
    echo "Файл ../ex00/hh.json не найден"
    exit 1
fi

jq -r -f filter.jq ../ex00/hh.json > hh.csv

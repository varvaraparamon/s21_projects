#!/bin/bash

if [ ! -f data.txt ]; then
    echo "Файл data.txt не найден."
    exit 1
fi

termgraph data.txt --width=60 --color green red
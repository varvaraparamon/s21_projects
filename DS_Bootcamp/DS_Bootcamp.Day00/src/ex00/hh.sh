#!/bin/sh

if [ $# -eq 0 ]; then
  echo "Usage: $0 <vacancy_name>"
  exit 1
fi

VACANCY_NAME=""

for word in "$@"; do
  if [ -n "$VACANCY_NAME" ]; then
    VACANCY_NAME="$VACANCY_NAME+$word"
  else
    VACANCY_NAME="$word"
  fi
done

API_URL="https://api.hh.ru/vacancies"
PARAMS="text=${VACANCY_NAME}"

curl -s "$API_URL?$PARAMS" | jq '.' > hh.json
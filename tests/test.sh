#!/bin/bash

for ((i=0; i < 10; i++))
do
  echo "Start $i curl\n"
  curl --location 'http://localhost:8000/api/v1/add/' \
      --header 'Content-Type: application/json' \
      --data '{
        "expression": "((7+1)/(2+2)*4)/8*(32-((4+12)*2))-1+((7+1)/(2+2)*4)/8*(32-((4+12)*2))-1"
        }'
done

exit 0

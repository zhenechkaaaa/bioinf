#!/bin/bash

FLAGSTAT=$1

RATE=$(grep " mapped (" "$FLAGSTAT" \
| head -1 \
| sed -E 's/.*\(([0-9.]+)%.*/\1/')

echo "Mapping rate = $RATE %"

RESULT=$(echo "$RATE > 90" | bc)

if [ "$RESULT" -eq 1 ]
then
    echo "OK"
else
    echo "not OK"
fi

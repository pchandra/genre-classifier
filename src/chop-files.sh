#!/usr/bin/bash

for i in *; do \
    echo "$i"
    cd "$i"
    mkdir -p out
    for j in *.mp3; do \
        echo "PROCESSING $i/$j"
        ~/wav-mixer/trim-chopper.py -o out "$j"
    done
done

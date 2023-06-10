#!/bin/bash

GENRE="$1"
FILE="$2"
pushd . >/dev/null 2>&1
cd ~/genre-classifier
python3 src/get_genre.py model/$GENRE.pt $GENRE "$FILE"
popd >/dev/null 2>&1

#! /bin/bash

PLAYER="pi/player.py"
SONGS_DIR="MIDI/"

SONGS=($(find "$SONGS_DIR" -type f -iname "*.mid"))
SONG="${SONGS[RANDOM % ${#SONGS[@]}]}"

python $PLAYER $SONG

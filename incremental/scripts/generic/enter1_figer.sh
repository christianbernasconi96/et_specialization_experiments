#!/bin/bash

while getopts "p:" opt; do
  case $opt in
    p) PROJECTOR = $opt
  esac
done

bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f art
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f broadcast
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f building
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f computer
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f education
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f event
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f finance
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f geography
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f government
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f internet
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f living_thing
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f location
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f medicine
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f metropolitan_transit
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f organization
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f people
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f person
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f product
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f rail
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f religion
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f transportation
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f visual_art
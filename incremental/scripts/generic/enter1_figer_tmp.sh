#!/bin/bash

COPY_FATHER=''

while getopts "p:c" opt; do
  case $opt in
    p) PROJECTOR=$OPTARG
    ;;
    c) COPY_FATHER='-c'
    ;;
  esac
done

# bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f art $COPY_FATHER
# bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f broadcast $COPY_FATHER
# bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f building $COPY_FATHER
# bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f education $COPY_FATHER
# bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f event $COPY_FATHER
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f computer $COPY_FATHER
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f geography $COPY_FATHER
# bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f government $COPY_FATHER
# bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f living_thing $COPY_FATHER
# bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f location $COPY_FATHER
# bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f organization $COPY_FATHER
# bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f finance $COPY_FATHER
# bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f internet $COPY_FATHER
# bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f medicine $COPY_FATHER
# bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f metropolitan_transit $COPY_FATHER
# bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f people $COPY_FATHER
# bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f person $COPY_FATHER
# bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f product $COPY_FATHER
# bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f rail $COPY_FATHER
# bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f religion $COPY_FATHER
# bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f transportation $COPY_FATHER
# bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D figer -f visual_art $COPY_FATHER
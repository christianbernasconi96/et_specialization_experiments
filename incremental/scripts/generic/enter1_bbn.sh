#!/bin/bash

while getopts "p:" opt; do
  case $opt in
    p) PROJECTOR=$OPTARG
    ;;
  esac
done

bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D bbn -f CONTACT_INFO
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D bbn -f EVENT
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D bbn -f FACILITY
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D bbn -f GPE
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D bbn -f LOCATION
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D bbn -f ORGANIZATION
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D bbn -f PRODUCT
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D bbn -f SUBSTANCE
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D bbn -f WORK_OF_ART
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

bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D bbn -f CONTACT_INFO $COPY_FATHER
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D bbn -f EVENT $COPY_FATHER
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D bbn -f FACILITY $COPY_FATHER
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D bbn -f GPE $COPY_FATHER
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D bbn -f LOCATION $COPY_FATHER
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D bbn -f ORGANIZATION $COPY_FATHER
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D bbn -f PRODUCT $COPY_FATHER
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D bbn -f SUBSTANCE $COPY_FATHER
bash incremental/scripts/generic/run_all_$PROJECTOR.sh -D bbn -f WORK_OF_ART $COPY_FATHER
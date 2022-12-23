#!/bin/bash

while getopts "f:lD:" opt; do
  case $opt in
    f) FAMILY=$OPTARG
    ;;
    D) DATA=$OPTARG
  esac
done
# read
unzip /home/remote_hdd/tokenized_datasets/$DATA/specialization/incremental/$FAMILY.zip -d /home/remote_hdd/tokenized_datasets/$DATA/specialization/incremental/;
bash incremental/scripts/generic_onto_tmp/run_all.sh -D $DATA -f $FAMILY -l
rm -r /home/remote_hdd/tokenized_datasets/$DATA/specialization/incremental/$FAMILY/
# read
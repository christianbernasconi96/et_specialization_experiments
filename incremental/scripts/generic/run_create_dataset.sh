#!/bin/bash

while getopts "f:D:" opt; do
  case $opt in
    f) FAMILY=$OPTARG
    ;;
    D) DATA=$OPTARG
    ;;
  esac
done


# eventually set modality: Load
DATA_CONFIG_PATH='incremental/configs/data/'$DATA'_'$FAMILY'_subset_X_instance_Y.yaml'
sed -i 's/: Load/: CreateAndSave/g' $DATA_CONFIG_PATH
# CLASSIFIER
bash incremental/scripts/generic/run_all_classifier.sh -D $DATA -f $FAMILY
# set modality: Load
sed -i 's/: CreateAndSave/: Load/g' $DATA_CONFIG_PATH
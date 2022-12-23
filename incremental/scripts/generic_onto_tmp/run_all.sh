#!/bin/bash

MODALITY='CreateAndSave'

while getopts "f:lD:" opt; do
  case $opt in
    f) FAMILY=$OPTARG
    ;;
    l) MODALITY='Load'
    ;;
    D) DATA=$OPTARG
  esac
done

# eventually set modality: Load
DATA_CONFIG_PATH='incremental/configs/data/'$DATA'_'$FAMILY'_subset_X_instance_Y.yaml'
sed -i 's/: Load/: CreateAndSave/g' $DATA_CONFIG_PATH
sed -i 's/: CreateAndSave/: '$MODALITY'/g' $DATA_CONFIG_PATH
# CLASSIFIER
bash incremental/scripts/generic_onto_tmp/run_all_classifier.sh -D $DATA -f $FAMILY
# set modality: Load
sed -i 's/: CreateAndSave/: Load/g' $DATA_CONFIG_PATH

# run with Load
# BOX
bash incremental/scripts/generic_onto_tmp/run_all_box.sh -D $DATA -f $FAMILY

### KENN 
# VERTICAL
bash incremental/scripts/generic_onto_tmp/run_all_kenn_vertical.sh -D $DATA -f $FAMILY
# HORIZONTAL
bash incremental/scripts/generic_onto_tmp/run_all_kenn_horizontal.sh -D $DATA -f $FAMILY
# HORIZONTAL VERTICAL
# bash incremental/scripts/generic_onto_tmp/run_all_kenn_horizontal_vertical.sh -D $DATA -f $FAMILY

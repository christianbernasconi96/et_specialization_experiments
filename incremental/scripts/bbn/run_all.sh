#!/bin/bash

MODALITY='CreateAndSave'

while getopts "f:l" opt; do
  case $opt in
    f) FAMILY=$OPTARG
    ;;
    l) MODALITY='Load'
    ;;
  esac
done

# eventually set modality: Load
DATA_CONFIG_PATH='incremental/configs/data/bbn_'$FAMILY'_subset_X_instance_Y.yaml'
sed -i 's/Load/CreateAndSave/g' $DATA_CONFIG_PATH
sed -i 's/CreateAndSave/'$MODALITY'/g' $DATA_CONFIG_PATH
# CLASSIFIER
bash incremental/scripts/bbn/run_all_classifier.sh -f $FAMILY
# set modality: Load
sed -i 's/CreateAndSave/Load/g' $DATA_CONFIG_PATH

# run with Load
# BOX
bash incremental/scripts/bbn/run_all_box.sh -f $FAMILY

### KENN 
# VERTICAL
bash incremental/scripts/bbn/run_all_kenn_vertical.sh -f $FAMILY
# HORIZONTAL
bash incremental/scripts/bbn/run_all_kenn_horizontal.sh -f $FAMILY
# HORIZONTAL VERTICAL
bash incremental/scripts/bbn/run_all_kenn_horizontal_vertical.sh -f $FAMILY

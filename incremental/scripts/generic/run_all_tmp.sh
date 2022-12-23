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
# bash incremental/scripts/generic/run_all_classifier.sh -D $DATA -f $FAMILY
# set modality: Load
sed -i 's/: CreateAndSave/: Load/g' $DATA_CONFIG_PATH



for e in 'bottom_up' 'top_down' 'hybrid'
do
  bash incremental/scripts/generic/train_kenn_adapter_bert_ms.sh -s 0 -i 2 -k 20 -e $e -D bbn -f GPE
done



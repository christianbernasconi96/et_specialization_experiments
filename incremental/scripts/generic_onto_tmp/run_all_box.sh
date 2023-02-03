#!/bin/bash

while getopts "f:D:" opt; do
  case $opt in
    f) FAMILY=$OPTARG
    ;;
    D) DATA=$OPTARG
    ;;
  esac
done

# read -n 1 -s -r -p $'Modify CreateAndSave into Load in rw_options \n'
# run with Load
for i in $(seq 0 2)
do
  bash incremental/scripts/generic_onto_tmp/train_box_adapter_bert_ms.sh -s 0 -i $i -k 40 -D $DATA -f $FAMILY
done
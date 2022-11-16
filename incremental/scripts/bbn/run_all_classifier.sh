#!/bin/bash

while getopts "f:" opt; do
  case $opt in
    f) FAMILY=$OPTARG
  esac
done


# read -n 1 -s -r -p $'Modify Load into CreateAndSave in rw_options \n'
for i in $(seq 0 2)
do
  # run CreateAndSave 
  for k in 10 20 40
  do
    bash incremental/scripts/bbn/train_classifier_adapter_bert_ms.sh -s 0 -i $i -k $k -f $FAMILY
  done
done
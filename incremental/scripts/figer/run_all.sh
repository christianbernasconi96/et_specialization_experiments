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
    bash incremental/scripts/figer/train_classifier_adapter_bert_ms.sh -s 0 -i $i -k $k -f $FAMILY
  done
done

# read -n 1 -s -r -p $'Modify CreateAndSave into Load in rw_options \n'
# run with Load
for i in $(seq 0 2)
do
  for k in 10 20 40
  do
    bash incremental/scripts/figer/train_box_adapter_bert_ms.sh -s 0 -i $i -k $k -f $FAMILY
    for e in 'bottom_up' 'top_down' 'hybrid'
    do
      bash incremental/scripts/figer/train_kenn_adapter_bert_ms.sh -s 0 -i $i -k $k -e $e -f $FAMILY
    done
  done
done
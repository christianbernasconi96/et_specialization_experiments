#!/bin/bash

COPY_FATHER=''

while getopts "f:D:c" opt; do
  case $opt in
    f) FAMILY=$OPTARG
    ;;
    D) DATA=$OPTARG
    ;;
    c) COPY_FATHER='-c'
    ;;
  esac
done


# read -n 1 -s -r -p $'Modify Load into CreateAndSave in rw_options \n'
for i in $(seq 0 2)
do
  # run CreateAndSave 
  for k in 10 20 40
  do
    bash incremental/scripts/generic_onto/train_classifier_adapter_bert_ms.sh -s 0 -i $i -k $k -D $DATA -f $FAMILY $COPY_FATHER
  done
done
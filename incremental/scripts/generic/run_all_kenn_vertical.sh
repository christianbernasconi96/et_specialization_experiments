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

# read -n 1 -s -r -p $'Modify CreateAndSave into Load in rw_options \n'
# run with Load
for i in $(seq 0 2)
do
  for k in 10 20 40
  do
    for e in 'bottom_up' 'top_down' 'hybrid'
    do
      bash incremental/scripts/generic/train_kenn_adapter_bert_ms.sh -s 0 -i $i -k $k -e $e -D $DATA -f $FAMILY $COPY_FATHER
    done
  done
done
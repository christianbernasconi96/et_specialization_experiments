#!/bin/bash

while getopts "f:" opt; do
  case $opt in
    f) FAMILY=$OPTARG
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
      bash incremental/scripts/bbn/train_kenn_adapter_bert_ms.sh -s 0 -i $i -k $k -e $e -f $FAMILY
    done
  done
done
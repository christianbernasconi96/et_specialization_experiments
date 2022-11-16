#!/bin/bash

while getopts "f:" opt; do
  case $opt in
    f) FAMILY=$OPTARG
  esac
done
# tmp
for k in 20 40
do
  for e in 'bottom_up' 'top_down' 'hybrid'
  do
    bash incremental/scripts/figer/train_kenn_adapter_bert_ms.sh -s 0 -i 1 -k $k -e $e -f $FAMILY
  done
done
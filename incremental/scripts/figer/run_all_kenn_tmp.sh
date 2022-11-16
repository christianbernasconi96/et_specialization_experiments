#!/bin/bash

while getopts "f:" opt; do
  case $opt in
    f) FAMILY=$OPTARG
  esac
done



for e in 'top_down' 'hybrid'
do
  bash incremental/scripts/figer/train_kenn_adapter_bert_ms.sh -s 0 -i 1 -k 10 -e $e -f $FAMILY
done


for k in 10 20 40
do
  for e in 'bottom_up' 'top_down' 'hybrid'
  do
    bash incremental/scripts/figer/train_kenn_adapter_bert_ms.sh -s 0 -i 2 -k $k -e $e -f $FAMILY
  done
done

#!/bin/bash

while getopts "f:" opt; do
  case $opt in
    f) FAMILY=$OPTARG
  esac
done

# kenn horizontal
for i in $(seq 0 2)
do
  for k in 10 20 40
  do
    bash incremental/scripts/figer/train_kenn_horizontal_adapter_bert_ms.sh -s 0 -i $i -k $k -f $FAMILY
  done
done
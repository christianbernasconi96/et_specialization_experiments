#!/bin/bash
bash incremental/scripts/generic/train_classifier_adapter_bert_ms.sh -s 0 -i 1 -k 10 -D figer -f event
bash incremental/scripts/generic/train_classifier_adapter_bert_ms.sh -s 0 -i 0 -k 40 -D figer -f event
bash incremental/scripts/generic/train_classifier_adapter_bert_ms.sh -s 0 -i 2 -k 40 -D figer -f event
bash incremental/scripts/generic/run_all_tmp.sh -D figer -f religion -l
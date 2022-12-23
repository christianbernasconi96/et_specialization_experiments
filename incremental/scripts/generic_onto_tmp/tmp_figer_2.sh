#!/bin/bash
bash incremental/scripts/generic_onto_tmp/run_all_classifier.sh -D figer -f metropolitan_transit
bash incremental/scripts/generic_onto_tmp/run_all_kenn_vertical.sh -D figer -f metropolitan_transit
bash incremental/scripts/generic_onto_tmp/run_all_box.sh -D figer -f metropolitan_transit
bash incremental/scripts/generic_onto_tmp/run_all_classifier.sh -D figer -f government
bash incremental/scripts/generic_onto_tmp/run_all_kenn_vertical.sh -D figer -f government
bash incremental/scripts/generic_onto_tmp/run_all_box.sh -D figer -f government
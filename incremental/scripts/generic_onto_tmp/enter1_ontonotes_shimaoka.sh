#!/bin/bash

while getopts "p:" opt; do
  case $opt in
    p) PROJECTOR=$OPTARG
  esac
done

bash incremental/scripts/generic_onto_tmp/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f location_geography
bash incremental/scripts/generic_onto_tmp/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f location_structure
bash incremental/scripts/generic_onto_tmp/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f location_transit
bash incremental/scripts/generic_onto_tmp/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f organization_company
bash incremental/scripts/generic_onto_tmp/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f other_art

# NOTE: be careful, there sports_event is missing from subset_40
# bash incremental/scripts/generic_onto_tmp/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f other_event

bash incremental/scripts/generic_onto_tmp/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f other_health
bash incremental/scripts/generic_onto_tmp/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f other_language
bash incremental/scripts/generic_onto_tmp/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f other_living_thing
bash incremental/scripts/generic_onto_tmp/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f other_product
bash incremental/scripts/generic_onto_tmp/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f person_artist
#!/bin/bash

COPY_FATHER=''

while getopts "p:c" opt; do
  case $opt in
    p) PROJECTOR=$OPTARG
    ;;
    c) COPY_FATHER='-c'
    ;;
  esac
done

bash incremental/scripts/generic_onto/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f location_geography $COPY_FATHER
bash incremental/scripts/generic_onto/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f location_structure $COPY_FATHER
bash incremental/scripts/generic_onto/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f location_transit $COPY_FATHER
bash incremental/scripts/generic_onto/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f organization_company $COPY_FATHER
bash incremental/scripts/generic_onto/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f other_art $COPY_FATHER

# NOTE: be careful, there sports_event is missing from subset_40
# bash incremental/scripts/generic_onto/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f other_event $COPY_FATHER

bash incremental/scripts/generic_onto/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f other_health $COPY_FATHER
bash incremental/scripts/generic_onto/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f other_language $COPY_FATHER
bash incremental/scripts/generic_onto/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f other_living_thing $COPY_FATHER
bash incremental/scripts/generic_onto/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f other_product $COPY_FATHER
bash incremental/scripts/generic_onto/run_all_$PROJECTOR.sh -D ontonotes_shimaoka -f person_artist $COPY_FATHER
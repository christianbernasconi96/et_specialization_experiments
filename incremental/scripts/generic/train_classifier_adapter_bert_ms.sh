#!/bin/bash

CMD='python'
SEED=0
while getopts "ds:i:k:D:f:" opt; do
  case $opt in
    d) CMD='debugpy-run -p :5680'
    ;;
    s) SEED=$OPTARG
    ;;
    i) INSTANCE=$OPTARG
    ;;
    k) SUBSET=$OPTARG
    ;;
    D) DATA=$OPTARG
    ;;
    f) FAMILY=$OPTARG
    ;;
  esac
done

# prepare data yaml
DATA_CONFIG_TEMPLATE='incremental/configs/data/'$DATA'_'$FAMILY'_subset_X_instance_Y.yaml'
NEW_DATA_CONFIG_PATH='incremental/configs/data/generated_config_files/'$DATA'_'$FAMILY'_subset_'$SUBSET'_instance_'$INSTANCE'.yaml'
cp $DATA_CONFIG_TEMPLATE $NEW_DATA_CONFIG_PATH
sed -i 's/subset_X/subset_'$SUBSET'/g' $NEW_DATA_CONFIG_PATH
sed -i 's/instance_Y/instance_'$INSTANCE'/g' $NEW_DATA_CONFIG_PATH



$CMD incremental/trainers/trainer_bert.py fit \
--seed_everything=$SEED \
--data incremental/configs/data/common.yaml \
--data 'pretraining/configs/data/'$DATA'_bert_ms.yaml' \
--data $NEW_DATA_CONFIG_PATH \
--trainer incremental/configs/trainer_common.yaml \
--trainer.callbacks=ModelCheckpoint \
--trainer.callbacks.dirpath=/home/remote_hdd/trained_models/$DATA/specialization/incremental/$FAMILY/subset_$SUBSET/instance_$INSTANCE \
--trainer.callbacks.filename=classifier_adapter_bert_ms \
--trainer.callbacks.monitor=losses/val_loss \
--trainer.callbacks.save_weights_only=True \
--trainer.callbacks=EarlyStopping \
--trainer.callbacks.patience=5 \
--trainer.callbacks.monitor=losses/val_loss \
--trainer.callbacks.mode=min \
--trainer.callbacks.verbose=True \
--model incremental/configs/model/common.yaml \
--model 'incremental/configs/model/'$DATA'_classifier_bert.yaml' \
--model.checkpoint_to_load=/home/remote_hdd/trained_models/$DATA/specialization/pretraining/classifier_adapter_bert_ms.ckpt \
--logger incremental/configs/logger.yaml \
--logger.project=$DATA'_specialization_incremental_'$FAMILY'_subset'$SUBSET \
--logger.name=classifier_adapter_bert_ms
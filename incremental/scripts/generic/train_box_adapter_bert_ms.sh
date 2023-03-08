#!/bin/bash

CMD='python'
SEED=0
COPY_FATHER='False'
INIT_STRING='no_init_'
while getopts "ds:i:k:D:f:c" opt; do
  case $opt in
    d) CMD='debugpy-run -p :5681'
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
    c) COPY_FATHER='True' INIT_STRING='smart_init_'
    ;;
  esac
done

# prepare data yaml
DATA_CONFIG_TEMPLATE='incremental/configs/data/'$DATA'_'$FAMILY'_subset_X_instance_Y.yaml'
NEW_DATA_CONFIG_PATH='incremental/configs/data/generated_config_files/'$DATA'_'$FAMILY'_subset_'$SUBSET'_instance_'$INSTANCE'.yaml'
cp $DATA_CONFIG_TEMPLATE $NEW_DATA_CONFIG_PATH
sed -i 's/subset_X/subset_'$SUBSET'/g' $NEW_DATA_CONFIG_PATH
sed -i 's/instance_Y/instance_'$INSTANCE'/g' $NEW_DATA_CONFIG_PATH

# prepare model yaml
MODEL_CONFIG_TEMPLATE='incremental/configs/model/'$DATA'_box_bert.yaml'
NEW_MODEL_CONFIG_PATH='incremental/configs/model/generated_config_files/'$DATA'_box_bert.yaml'
cp $MODEL_CONFIG_TEMPLATE $NEW_MODEL_CONFIG_PATH
sed -i 's/CopyFatherFlag/'$COPY_FATHER'/g' $NEW_MODEL_CONFIG_PATH

$CMD incremental/trainers/trainer_box_bert.py fit \
--seed_everything=$SEED \
--data incremental/configs/data/common.yaml \
--data 'pretraining/configs/data/'$DATA'_bert_ms.yaml' \
--data $NEW_DATA_CONFIG_PATH \
--trainer incremental/configs/trainer_common.yaml \
--trainer.callbacks=ModelCheckpoint \
--trainer.callbacks.dirpath=/home/remote_hdd/trained_models/$DATA/specialization/incremental/$FAMILY/subset_$SUBSET/instance_$INSTANCE \
--trainer.callbacks.filename=$INIT_STRING'box_adapter_bert_ms' \
--trainer.callbacks.monitor=losses/val_loss \
--trainer.callbacks.save_weights_only=True \
--trainer.callbacks=EarlyStopping \
--trainer.callbacks.patience=5 \
--trainer.callbacks.monitor=losses/val_loss \
--trainer.callbacks.mode=min \
--trainer.callbacks.verbose=True \
--model incremental/configs/model/common.yaml \
--model $NEW_MODEL_CONFIG_PATH \
--model.checkpoint_to_load=/home/remote_hdd/trained_models/$DATA/specialization/pretraining/box_adapter_bert_ms.ckpt \
--logger incremental/configs/logger.yaml \
--logger.project=$DATA'_specialization_'$FAMILY'_subset'$SUBSET \
--logger.name=$INIT_STRING'box_adapter_bert_ms'
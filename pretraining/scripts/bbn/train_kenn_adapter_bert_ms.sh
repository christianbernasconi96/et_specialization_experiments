#!/bin/bash

CMD='python'
SEED=0
while getopts "ds:e:" opt; do
  case $opt in
    d) CMD='debugpy-run -p :5680'
    ;;
    s) SEED=$OPTARG
    ;;
    e) KB_ENCODING=$OPTARG
    ;;
  esac
done

# prepare model yaml
MODEL_CONFIG_TEMPLATE='pretraining/configs/model/kenn_X_bert.yaml'
NEW_MODEL_CONFIG_PATH='pretraining/configs/model/kenn_'$KB_ENCODING'_bert.yaml'
cp $MODEL_CONFIG_TEMPLATE $NEW_MODEL_CONFIG_PATH
sed -i 's/KB-encoding/'$KB_ENCODING'/g' $NEW_MODEL_CONFIG_PATH

$CMD pretraining/trainers/trainer_kenn_bert.py fit \
--seed_everything=$SEED \
--data pretraining/configs/data/common_bert.yaml \
--data pretraining/configs/data/bbn_bert_ms.yaml \
--trainer pretraining/configs/trainer_common.yaml \
--trainer.callbacks=ModelCheckpoint \
--trainer.callbacks.dirpath=/home/remote_hdd/trained_models/bbn/specialization/pretraining \
--trainer.callbacks.filename='kenn_'$KB_ENCODING'_adapter_bert_ms' \
--trainer.callbacks.monitor=val_loss \
--trainer.callbacks.save_weights_only=True \
--trainer.callbacks=EarlyStopping \
--trainer.callbacks.patience=5 \
--trainer.callbacks.monitor=val_loss \
--trainer.callbacks.mode=min \
--trainer.callbacks.verbose=True \
--model pretraining/configs/model/common.yaml \
--model pretraining/configs/model/kenn_common.yaml \
--model $NEW_MODEL_CONFIG_PATH \
--logger pretraining/configs/logger.yaml \
--logger.project=bbn_specialization_pretraining \
--logger.name='kenn_'$KB_ENCODING'_adapter_bert_ms'
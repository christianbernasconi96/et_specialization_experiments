#!/bin/bash

CMD='python'
SEED=0
while getopts "ds:" opt; do
  case $opt in
    d) CMD='debugpy-run -p :5680'
    ;;
    s) SEED=$OPTARG
    ;;
  esac
done


$CMD pretraining/trainers/trainer_bert.py fit \
--seed_everything=$SEED \
--data pretraining/configs/data/common_bert.yaml \
--data pretraining/configs/data/few_NERD_bert_ms.yaml \
--trainer pretraining/configs/trainer_common.yaml \
--trainer.callbacks=ModelCheckpoint \
--trainer.callbacks.dirpath=/home/remote_hdd/trained_models/few_NERD/specialization/pretraining \
--trainer.callbacks.filename=classifier_adapter_bert_ms \
--trainer.callbacks.monitor=val_loss \
--trainer.callbacks.save_weights_only=True \
--trainer.callbacks=EarlyStopping \
--trainer.callbacks.patience=5 \
--trainer.callbacks.monitor=val_loss \
--trainer.callbacks.mode=min \
--trainer.callbacks.verbose=True \
--model pretraining/configs/model/common.yaml \
--model pretraining/configs/model/classifier_bert.yaml \
--logger pretraining/configs/logger.yaml \
--logger.project=few_NERD_specialization_pretraining \
--logger.name=classifier_adapter_bert_ms
# %% imports and paths
import os

# set main directories
DATA = 'bbn'
SCENARIO = 'complete' # ['complete', 'single_child']
TRAIN_DATA = 'train.json'
DEV_DATA = 'dev.json'
SUBSET = 40
INSTANCE = 0
INCREMENTAL_DATA_DIR = f'/home/remote_hdd/datasets_for_incremental_training/{DATA}/{SCENARIO}_subset_{SUBSET}/instance_{INSTANCE}'
PRETRAINING_TYPES_PATH = f'/home/remote_hdd/tokenized_datasets/{DATA}/specialization/pretraining/types_list.txt'
DST_TYPES_DIR = f'/home/remote_hdd/tokenized_datasets/{DATA}/specialization/incremental/'
DST_TYPES_DIR = DST_TYPES_DIR + '{}'
DST_YAML_DIR = f'/home/cbernasconi/et/experiments/specialization/incremental/configs/data'
# %%
####### CREATE types_list.txt #########
# read pretraining types from file
types_pretraining = open(PRETRAINING_TYPES_PATH, 'r').read().splitlines()
types_pretraining
# %%
# extract incremental types from filesystem
father_childs = {}
for dirname in os.listdir(INCREMENTAL_DATA_DIR):
  father = f"/{dirname.replace('sons_of_', '')}"
  childs = []
  for filename in os.listdir(os.path.join(INCREMENTAL_DATA_DIR, dirname)):
    if 'train' in filename:
      child = f"{father}/{filename.replace('incremental_train_', '').replace('.json', '')}"
      childs.append(child)
  childs = sorted(childs)
  father_childs[father] = childs

father_childs

# %%
# save concatenated pretraining and incremental
for father, childs in father_childs.items():
  if childs:
    types_family = types_pretraining + childs
    dst_types_dir = DST_TYPES_DIR.format(father[1:])
    os.makedirs(dst_types_dir, exist_ok=True)
    dst_types_path = os.path.join(dst_types_dir, 'types_list.txt')
    with open(dst_types_path, 'w') as out:
      out.write('\n'.join(types_family))
      out.write('\n')
# %%
######### CREATE DATA yaml ###########
import yaml
from copy import deepcopy

base_yaml = {
  'dataset_paths' : {
    'pretraining_train': f'/home/remote_hdd/datasets_for_incremental_training/{DATA}/complete/pretraining_train_nodev.json',
    'pretraining_dev': f'/home/remote_hdd/datasets_for_incremental_training/{DATA}/complete/pretraining_dev.json',
    'pretraining_test': f'/home/remote_hdd/datasets_for_incremental_training/{DATA}/complete/pretraining_test.json',
  },
  'rw_options': {
      'modality': 'CreateAndSave',
      'light' : True
  },
  'dataloader_params' : {
    'name': 'torch.DataLoader',
    'pretraining_train' : {
      'batch_size' : 5,
      'shuffle' : True
    },
    'pretraining_dev' : {
      'batch_size': 64
    },
    'pretraining_test' : {
      'batch_size': 64
    }
  }
}

for family, childs in father_childs.items():
  if childs:
    family_suffix = family.split('/')[-1]
    # shared options
    family_yaml = deepcopy(base_yaml)
    family_yaml['rw_options']['dirpath'] = f'/home/remote_hdd/tokenized_datasets/{DATA}/specialization/incremental/{family_suffix}/subset_X/instance_Y/'
    family_yaml['rw_options']['types_list_path'] = f'/home/remote_hdd/tokenized_datasets/{DATA}/specialization/incremental/{family_suffix}/types_list.txt'
    for child in childs:
      child_suffix = child.split('/')[-1]
      # DATALOADER PARAMS
      # incremental train
      incremental_train_key = f'incremental_train.{child_suffix}'
      incremental_train_value = { 'batch_size' : 5, 'shuffle' : True}
      family_yaml['dataloader_params'][incremental_train_key] = incremental_train_value
      # incremental dev
      incremental_dev_key = f'incremental_dev.{child_suffix}'
      incremental_dev_value = { 'batch_size' : 5}
      family_yaml['dataloader_params'][incremental_dev_key] = incremental_dev_value
      # DATASET PATHS
      family_yaml['dataset_paths'][incremental_train_key] = f'/home/remote_hdd/datasets_for_incremental_training/{DATA}/complete_subset_X/instance_Y/sons_of_{family_suffix}/incremental_train_{child_suffix}.json'
      family_yaml['dataset_paths'][incremental_dev_key] = f'/home/remote_hdd/datasets_for_incremental_training/{DATA}/complete_subset_X/instance_Y/sons_of_{family_suffix}/incremental_dev_{child_suffix}.json'
    # save test path here to reserve the last idx
    family_yaml['dataset_paths']['test'] = f'/home/remote_hdd/datasets_for_incremental_training/{DATA}/test.json'
    family_yaml['dataloader_params']['test'] = { 'batch_size' : 64}

    # save config
    filename = f"{DATA}_{family_suffix}_subset_X_instance_Y.yaml"
    dst_yaml_path = os.path.join(DST_YAML_DIR, filename)
    with open(dst_yaml_path, 'w') as out:
      yaml.dump(family_yaml, out, sort_keys=False)
# %%

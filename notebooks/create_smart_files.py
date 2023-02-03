# %% imports and paths
import os
import json
from tqdm import tqdm
import entity_typing_framework.EntityTypingNetwork_classes.KENN_networks.kenn_utils as kenn_utils

# set main directories
DATA = 'ontonotes_shimaoka'
SCENARIO = 'complete' # ['complete', 'single_child']
TRAIN_DATA = 'train.json'
DEV_DATA = 'dev.json'
SUBSET = 10
INSTANCE = 0
INCREMENTAL_DATA_DIR = f'/home/remote_hdd/datasets_for_incremental_training/{DATA}/{SCENARIO}_subset_{SUBSET}/instance_{INSTANCE}'
PRETRAINING_TYPES_PATH = f'/home/remote_hdd/tokenized_datasets/{DATA}/specialization/pretraining/types_list.txt'
DST_TYPES_DIR = f'/home/remote_hdd/tokenized_datasets/{DATA}/specialization/incremental'
DST_TYPES_DIR = DST_TYPES_DIR + '/{}'
DST_YAML_DIR = f'/home/cbernasconi/et/experiments/specialization/incremental/configs/data'
DST_KB_DIR = f'/home/cbernasconi/et/experiments/specialization/kenn_tmp/{DATA}'
DST_KB_DIR = DST_KB_DIR + '/{}'
ORIGINAL_DATA_DIR = f'/home/remote_hdd/datasets/{DATA}/'
INCREMENTAL_TYPES_LIST_PATH = f'/home/remote_hdd/tokenized_datasets/{DATA}/specialization/incremental'
INCREMENTAL_TYPES_LIST_PATH = INCREMENTAL_TYPES_LIST_PATH + '/{}/types_list.txt'
KB_MODE = ['bottom_up', 'top_down', 'hybrid']
FAMILY = {
  'bbn' : [
    'CONTACT_INFO',
          'EVENT',
          'FACILITY',
          'GPE',
          'LOCATION',
          'ORGANIZATION',
          'PRODUCT',
          'SUBSTANCE',
          'WORK_OF_ART'],
  'figer' : ['art',
            'broadcast',
            'building',
            'computer',
            'education',
            'event',
            'finance',
            'geography',
            'government',
            'internet',
            'living_thing',
            'location',
            'medicine',
            'metropolitan_transit',
            'organization',
            'people',
            'person',
            'product',
            'rail',
            'religion',
            'transportation',
            'visual_art'],
  'ontonotes_shimaoka': [
    'location/geography',
    'location/structure',
    'location/transit',
    'organization/company',
    'other/art',
    'other/event',
    'other/health',
    'other/language',
    'other/living_thing',
    'other/product',
    'person/artist'
  ]
}
# %%
####### CREATE types_list.txt #########
# read pretraining types from file
types_pretraining = open(PRETRAINING_TYPES_PATH, 'r').read().splitlines()
types_pretraining
# %%
# extract incremental types from filesystem
father_childs = {}
for dirname in os.listdir(INCREMENTAL_DATA_DIR):
  # TODO: check the next two lines...
  father = f"/{dirname.replace('sons_of_', '')}"
  if DATA == 'ontonotes_shimaoka':
    father = father.split('_')[0] + '/' + '_'.join(father.split('_')[1:])
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
    dst_types_dir = DST_TYPES_DIR.format(father[1:].replace('/', '_'))
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
    family_suffix = family[1:].replace('/', '_')
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
######### CREATE horizontal kbs ###########
# read types from data
with open(os.path.join(ORIGINAL_DATA_DIR, 'train.json'), 'r') as inp:
    dataset_types = [json.loads(l)['y_str'] for l in tqdm(inp.readlines())]
# read types from ontology
with open(os.path.join(ORIGINAL_DATA_DIR, 'all_types.txt'), 'r') as inp:
    types = [l.replace('\n', '') for l in inp.readlines()] 

types.sort()
type2id = {t:i for i, t in enumerate(types)}
# %%
# count cooccurencies
cooccurrence_counter = {t1: { t2: 0 for t2 in types } for t1 in types}
for dataset_type in tqdm(dataset_types):
    for t1 in dataset_type:
        for t2 in dataset_type:
            cooccurrence_counter[t1][t2] += 1


# keep track of non-cooccurent pairs
tupled_pairs = []
for t1 in cooccurrence_counter:
    for t2, c in cooccurrence_counter[t1].items():
        if c == 0:
            t1t2 = [t1, t2]
            t1t2.sort()
            if t1t2 not in tupled_pairs:
                tupled_pairs.append((t1t2))
tupled_pairs

# %%
for family in FAMILY[DATA]:
  # filter pairs by family
  type_to_filter = f'/{family}'
  filtered_pairs = [p for p in tupled_pairs if type_to_filter in p[0] or type_to_filter in p[1]]
  filtered_pairs

  # get trasversal pairs
  trasversal_pairs = []

  for t1, t2 in filtered_pairs:
      if type_to_filter in t1:
          father_t = '/'.join(t2.split('/')[:-1])
          trasversal_pair = [father_t, t1]
      elif type_to_filter in t2:
          father_t = '/'.join(t1.split('/')[:-1])
          trasversal_pair = [father_t, t2]
      
      if trasversal_pair not in trasversal_pairs:
          trasversal_pairs.append(trasversal_pair)

  # keep pairs involving only subtypes of the family (discard subtypes from other families)
  incremental_types_list_path = INCREMENTAL_TYPES_LIST_PATH.format(family.replace('/', '_'))
  types_to_keep = open(incremental_types_list_path).read().splitlines()

  pairs = []

  for t1, t2 in trasversal_pairs:
      if t1 in types_to_keep and t2 in types_to_keep:
          # if not (t1 == type_to_filter and type_to_filter in t2 or t2 == type_to_filter and type_to_filter in t1):
          if (not (t1 == type_to_filter and type_to_filter in t2 or t2 == type_to_filter and type_to_filter in t1)) or (t1 != type_to_filter and t2 != type_to_filter and type_to_filter in t1 and type_to_filter in t2):
              t1t2 = [t1, t2]    
              t1t2.sort()        
              pair = f'_:nP{t1t2[0]},nP{t1t2[1]}'

              if pair not in pairs:
                  pairs.append(pair)

  # create horizontal KB
  predicates = ','.join([f'P{t}' for t in types_to_keep])
  horizontal_clauses = '\n'.join(pairs)
  horizontal_kb = predicates + '\n\n' + horizontal_clauses + '\n'
  # save KB
  filename = f'horizontal.txt'
  dst_kb_dir = DST_KB_DIR.format(family)
  os.makedirs(dst_kb_dir, exist_ok=True)
  with open(os.path.join(dst_kb_dir, filename), 'w') as out:
      out.write(horizontal_kb)

  # create horizontal_vertical KB
  family_types = [t for t in types_to_keep if t.startswith(type_to_filter)]
  tree = kenn_utils.create_tree(family_types, label2pred = True)
  for kb_mode in KB_MODE:
    method = f"kenn_utils.generate_{kb_mode}"
    vertical_clauses = eval(method)(tree, '_')
    clauses = horizontal_clauses + '\n' + vertical_clauses
    kb = predicates + '\n\n' + clauses
    # save KB
    filename = f'horizontal_{kb_mode}.txt'
    dst_kb_dir = DST_KB_DIR.format(family)
    with open(os.path.join(dst_kb_dir, filename), 'w') as out:
        out.write(kb)


# %%


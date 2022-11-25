import sys
sys.path.append('..')

# imports
import os
import numpy as np
import json 
from tqdm import tqdm
import pandas as pd
from collections import defaultdict
from copy import deepcopy
import shutil
import random

SEED = [0, 1, 2]
# NOTE: to obtain the X-shot from the sota, set MIN_FREQ=2*X and TRAIN_RATIO=0.5
MIN_FREQ = 40 # 10 20 40
TRAIN_RATIO = 0.5
# set main directories
DATA = 'bbn' # figer
SCENARIO = 'complete' # ['complete', 'single_child']
TRAIN_DATA = 'train.json'
DEV_DATA = 'dev.json'
TEST_DATA = f"test{'-12k' if DATA == 'bbn' else ''}.json"
SRC_DATA_DIR = f'/home/remote_hdd/datasets_for_incremental_training/{DATA}/{SCENARIO}'
# DST_DATA_DIR = os.path.expanduser(f'./{DATA}/complete')
DST_DATA_DIR = f'/home/remote_hdd/datasets_for_incremental_training/{DATA}/{SCENARIO}_subset_{MIN_FREQ}'
DST_DATA_DIR = os.path.join(DST_DATA_DIR, 'instance_{}')
ONTOLOGY_PATH = f'/home/remote_hdd/datasets_for_incremental_training/{DATA}/all_types.txt'

# iterate over incremental training dirs
for dir in tqdm(os.listdir(SRC_DATA_DIR)):
  dirpath_src = os.path.join(SRC_DATA_DIR, dir)
  if os.path.isdir(dirpath_src):
    # iterate over incremental training single partitions
    for f in os.listdir(os.path.join(SRC_DATA_DIR, dir)):
      filepath_src = os.path.join(dirpath_src, f)
      print('Processing ', filepath_src, '...')
      with open(filepath_src, 'r') as src:
        lines = src.readlines()
        # check frequency
        if len(lines) >= MIN_FREQ:
          print('Type kept')
          # create an instance of the incremental dataset for each seed
          for seed in SEED:
            print('Creating instance of the dataset for seed', seed)
            # prepare dir
            dirpath_dst = os.path.join(DST_DATA_DIR.format(seed), dir)
            if not os.path.exists(dirpath_dst):
              os.makedirs(dirpath_dst, exist_ok=True)
            
            # save subset partitions
            filepath_train_dst = os.path.join(dirpath_dst, f)
            filepath_dev_dst = os.path.join(dirpath_dst, f.replace('_train_', '_dev_'))
            with open(filepath_train_dst, 'w') as dst_train, open(filepath_dev_dst, 'w') as dst_dev:
              # IMPORTANT: reset seed
              random.seed(seed)
              random.shuffle(lines)
              idx_split = int(MIN_FREQ * TRAIN_RATIO)
              train_lines = lines[:idx_split]
              dev_lines = lines[-idx_split:]
              # save
              dst_train.writelines(train_lines)
              dst_dev.writelines(dev_lines)
        else:
          print('Type discarded')
        print()
  else:
    # copy other files
    # shutil.copyfile(dirpath_src, os.path.join(DST_DATA_DIR, dir))
    pass


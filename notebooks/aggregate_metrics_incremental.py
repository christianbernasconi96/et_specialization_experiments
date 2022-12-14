# %% 
# %%
import os
import pandas as pd

DATA=['figer', 'bbn']
DATA = ['bbn']
FAMILY = {
  'bbn' : [
    'CONTACT_INFO',
          'EVENT',
          'FACILITY',
          # 'GPE',
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
            'visual_art']
}

# FAMILY = {
#   'bbn' : ['CONTACT_INFO']
# }

SUBSET = [10, 20, 40]
# SUBSET = [10]
INSTANCE = [0, 1, 2]

# set paths
MODEL_PATH = '/home/remote_hdd/trained_models/{data}/specialization/incremental/{family}/subset_{subset}/instance_{instance}/{model}_adapter_bert_ms.ckpt'
SRC_DIR_PATH = '../incremental/results/manual_test/{family}'
SRC_FILE = 'metrics_subset{subset}.csv'
OUT_FILE = 'metrics_subset{subset}_aggregated.csv'


# %%
for data in DATA:
  for family in FAMILY[data]:
    
    src_dir = SRC_DIR_PATH.format(family=family)
    out_dir = SRC_DIR_PATH.format(family=family)

    for subset in SUBSET:
      
      src_file = SRC_FILE.format(subset=subset)
      src_file_path = os.path.join(src_dir, src_file)
      out_file = OUT_FILE.format(subset=subset)
      out_file_path = os.path.join(out_dir, out_file)
      df = pd.read_csv(src_file_path)
      df = df.drop('instance', axis=1)
      cols = df.columns[1:]
      df_mean = df.groupby('projector').mean()
      df_mean.columns = [f'{c}/mean' for c in cols]
      df_std = df.groupby('projector').std()
      df_std.columns = [f'{c}/std' for c in cols]
      df_aggregated = pd.DataFrame.join(df_mean, df_std)
      df_aggregated.to_csv(out_file_path, index=True)




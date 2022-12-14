# %%
import wandb
import os
import pandas as pd
import json 
import warnings
warnings.filterwarnings('ignore')

wandb_api = wandb.Api()
WANDB_ENTITY = 'insides-lab-unimib-wandb'
WANDB_PROJECT = '{data}_specialization_incremental_{family}_subset{subset}'

N_INSTANCES = 3

DATA=['figer', 'bbn']
DATA=['bbn']
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
            'visual_art']
}

SUBSET = [10, 20, 40]

# set paths
OUT_DIR_PATH = '../incremental/results/wandb_export/{family}'
OUT_FILE = 'metrics_subset{subset}.csv'
OUT_FILE_AGGREGATED = 'metrics_subset{subset}_aggregated.csv'

# %%
def key_ok(key):
  return key.startswith('test') or key == 'epoch' or 'threshold' in key

# %%

for data in DATA:
  for family in FAMILY[data]:
    # prepare out dir
    out_dir = OUT_DIR_PATH.format(family=family)
    os.makedirs(out_dir, exist_ok=True)


    for subset in SUBSET:
      # get runs from wandb
      wandb_project = WANDB_PROJECT.format(data=data, family=family, subset=subset)
      wandb_path = f'{WANDB_ENTITY}/{wandb_project}'
      print('Processing runs from', wandb_path)
      runs = wandb_api.runs(wandb_path)
      
      # save metrics for each run
      df = pd.DataFrame()
      for run in runs:
        run_id = run.id
        name = run.name
        config = json.loads(run.json_config)
        # skip empty run
        if config:
          summary = run.summary
          instance = config['fit']['value']['data']['rw_options']['dirpath'].split('/')[-2].split('_')[-1]
          metrics = { k : v for k,v in summary.items() if key_ok(k) }
          row = {
            'name' : name,
            'instance' : instance,
            'run_id' : run_id
          }
          row.update(metrics)

          if len(df) > 0:
            df = df.append(row, ignore_index=True)
          else:
            df = pd.DataFrame([row])
        else:
          print('Empty run detected! Run details:')
          print('- url:', f'https://wandb.ai/{wandb_path}/runs/{run_id}')
          print('- name:', name)
          print('- instance:', instance)
      
      # check if the number of runs is correct
      if df[['name','instance']].groupby('name').count().mean().values[0] == N_INSTANCES:

        # prepare output      
        out_file = OUT_FILE.format(subset=subset)
        out_file_path = os.path.join(out_dir, out_file)

        # save csv
        df.to_csv(out_file_path, index=False)

        # prepare and save aggregated csv
        df = df.drop(['instance', 'run_id'], axis=1)
        cols = df.columns[1:]
        df_mean = df.groupby('name').mean()
        df_mean.columns = [f'{c}/mean' for c in cols]
        df_std = df.groupby('name').std()
        df_std.columns = [f'{c}/std' for c in cols]
        df_aggregated = pd.DataFrame.join(df_mean, df_std)
        out_file_aggregated = OUT_FILE_AGGREGATED.format(subset=subset)
        out_file_path_aggregated = os.path.join(out_dir, out_file_aggregated)
        df_aggregated.to_csv(out_file_path_aggregated, index=True)
      else:
        print('ATTENTION! NUMBER OF RUN IS NOT CORRECT!')
        print('Please check the project', f'https://wandb.ai/{wandb_path}')

# %%
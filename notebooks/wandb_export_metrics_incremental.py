# %%
import wandb
import os
import sys
import pandas as pd
import json 
import warnings
warnings.filterwarnings('ignore')


REDIRECT_LOG = True

wandb_api = wandb.Api()
WANDB_ENTITY = 'insides-lab-unimib-wandb'
# WANDB_PROJECT = '{data}_specialization_incremental_{family}_subset{subset}'
WANDB_PROJECT = '{data}_specialization_{family}_subset{subset}'

N_INSTANCES = 3

DATA=['figer', 'bbn', 'ontonotes_shimaoka']

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
          # 'other/event',
          'other/health',
          'other/language',
          'other/living_thing',
          'other/product',
          'person/artist'
  ]
}

SUBSET = [10, 20, 40]

# set paths
OUT_DIR_PATH = '../incremental/results/wandb_export/{data}/'
OUT_DIR_PATH_FAMILY = OUT_DIR_PATH + '{family}'
LOG_FILE_PATH = os.path.join('{}', 'log.txt')
OUT_FILE = 'metrics_subset{subset}.csv'
OUT_FILE_PROJECT_AGGREGATED = 'metrics_subset{subset}_aggregated.csv'
OUT_FILE_DATA = 'metrics.csv'
OUT_FILE_DATA_AGGREGATED = 'metrics_aggregated.csv'

# %%
def key_ok(key):
  return key.startswith('test') or key == 'epoch' or 'threshold' in key

# %%

for data in DATA:
  out_dir_data_path = OUT_DIR_PATH.format(data=data)
  os.makedirs(out_dir_data_path, exist_ok=True)
  
  if REDIRECT_LOG:
    sys.stdout = open(LOG_FILE_PATH.format(out_dir_data_path),'wt')
  
  print()
  print('####### Data', data,'######')
  # save metrics for each run
  df_data = pd.DataFrame(columns=['metric', 'projector', 'instance', 'family','subset',
                                  'precision', 'recall', 'f1', 'epoch'])
  df_data_aggregated = pd.DataFrame(columns=['metric', 'projector', 'family','subset',
                                  'precision/mean', 'recall/mean', 'f1/mean',
                                  'precision/std', 'recall/std', 'f1/std'])
  

  for family in FAMILY[data]:
    print()
    print('### FAMILY', family, '###')
    # prepare out dir
    out_dir_path_family = OUT_DIR_PATH_FAMILY.format(data=data, family=family.replace('/','_'))
    os.makedirs(out_dir_path_family, exist_ok=True)

    for subset in SUBSET:
      print()
      print('# SUBSET', subset, '#')
      # get runs from wandb
      wandb_project = WANDB_PROJECT.format(data=data, family=family.replace('/','_'), subset=subset)
      wandb_path = f'{WANDB_ENTITY}/{wandb_project}'
      print('Processing runs from', wandb_path)
      runs = wandb_api.runs(wandb_path)
      
      # save metrics for each run
      df_project = pd.DataFrame()
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

          if len(df_project) > 0:
            df_project = df_project.append(row, ignore_index=True)
          else:
            df_project = pd.DataFrame([row])
        else:
          if run.state != 'finished':
            print(f'{run.state.title()} run detected! Run details:')
          else:
            print('Empty run detected! Run details:')
          print('- url:', f'https://wandb.ai/{wandb_path}/runs/{run_id}')
          print('- name:', name)
          print('- instance:', instance)
      
      # check if the number of runs is correct
      if df_project[['name','instance']].groupby('name').count().mean().values[0] == N_INSTANCES:
        # replace NaN with 0
        df_project = df_project.replace('NaN', 0)

        # prepare output      
        out_file = OUT_FILE.format(subset=subset)
        out_file_path = os.path.join(out_dir_path_family, out_file)

        # save csv
        df_project.to_csv(out_file_path, index=False)

        # prepare and append row for df_data
        cols = list(df_project.columns)
        non_metrics_cols = ['threshold_incremental',
                            'threshold_pretraining',
                            'epoch', 'name', 'instance', 'run_id']
        cols_metrics = [c for c in cols if c not in non_metrics_cols]
        for i, df_row in df_project.iterrows():
          metric_base_keys = set([c.replace('/precision', '').replace('/recall', '').replace('/f1', '') for c in cols_metrics])
          for metric_base_key in metric_base_keys:
            row = {
              'projector': df_row['name'],
              'instance': df_row['instance'],
              'metric': metric_base_key,
              'family': family,
              'subset': subset,
              'precision': df_row[f'{metric_base_key}/precision'],
              'recall': df_row[f'{metric_base_key}/recall'],
              'f1': df_row[f'{metric_base_key}/f1'],
              'epoch': df_row['epoch']
            }

            df_data = df_data.append(row, ignore_index=True)
        
        # AGGREGATED METRICS
        # prepare and save aggregated csv
        df_project = df_project.drop(['instance', 'run_id'], axis=1)
        cols_mean = df_project.columns[1:]
        df_project_mean = df_project.groupby('name').mean()
        df_project_mean.columns = [f'{c}/mean' for c in cols_mean]
        df_project_std = df_project.groupby('name').std()
        df_project_std.columns = [f'{c}/std' for c in cols_mean]
        df_project_aggregated = pd.DataFrame.join(df_project_mean, df_project_std)
        out_file_project_aggregated = OUT_FILE_PROJECT_AGGREGATED.format(subset=subset)
        out_file_path_project_aggregated = os.path.join(out_dir_path_family, out_file_project_aggregated)
        df_project_aggregated.to_csv(out_file_path_project_aggregated, index=True)

        # prepare and append aggregated row for df_data_aggregated
        cols = list(df_project_aggregated.columns)
        non_metrics_cols = ['threshold_incremental/mean', 'threshold_incremental/std',
                            'threshold_pretraining/mean', 'threshold_incremental/std',
                            'epoch/mean', 'epoch/std']
        cols_mean = [c for c in cols if c.endswith('/mean') and c not in non_metrics_cols]
        for projector in df_project_aggregated.index:
          metric_base_keys = set([c.replace('/precision/mean', '').replace('/recall/mean', '').replace('/f1/mean', '') for c in cols_mean])
          for metric_base_key in metric_base_keys:
            row = {
              'projector': projector,
              'metric': metric_base_key,
              'family': family,
              'subset': subset,
              'precision/mean': df_project_aggregated.loc[projector, f'{metric_base_key}/precision/mean'],
              'recall/mean': df_project_aggregated.loc[projector, f'{metric_base_key}/recall/mean'],
              'f1/mean': df_project_aggregated.loc[projector, f'{metric_base_key}/f1/mean'],
              'precision/std': df_project_aggregated.loc[projector, f'{metric_base_key}/precision/std'],
              'recall/std': df_project_aggregated.loc[projector, f'{metric_base_key}/recall/std'],
              'f1/std': df_project_aggregated.loc[projector, f'{metric_base_key}/f1/std']
            }

            df_data_aggregated = df_data_aggregated.append(row, ignore_index=True)
      else:
        print('ATTENTION! NUMBER OF RUN IS NOT CORRECT!')
        print('Please check the project', f'https://wandb.ai/{wandb_path}')
  # save global dfs
  df_data.to_csv(f'{out_dir_data_path}/{OUT_FILE_DATA}', index=False)
  df_data_aggregated.to_csv(f'{out_dir_data_path}/{OUT_FILE_DATA_AGGREGATED}', index=False)

# %%

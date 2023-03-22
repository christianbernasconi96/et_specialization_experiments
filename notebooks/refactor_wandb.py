# %%
import wandb
import json 
import os
import sys

REDIRECT_LOG = True

# os.environ["WANDB_API_KEY"] = input('Insert wandb api key')
wandb_api = wandb.Api()
WANDB_ENTITY = 'insides-lab-unimib-wandb'
WANDB_PROJECT = '{data}_specialization_{family}_subset{subset}'
ACTION = 'CHECK_NAN' # ['DELETE', 'RENAME', 'CLEAN', 'CHECK_NAN]
PREFIX = 'smart_init_box_ad'
NEW_PREFIX = 'no_init_box'
DATA = ['figer', 'bbn'] # ['figer', 'bbn', 'ontonotes_shimaoka']
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

SUBSET = [10, 20, 40]

# %%


for data in DATA:
  if REDIRECT_LOG:
    sys.stdout = open(f'wandb_refactor_{data}_output.txt','wt')
  print()
  print('####### Data', data,'######')

  for family in FAMILY[data]:
    print()
    print('### FAMILY', family, '###')

    for subset in SUBSET:
      print()
      print('# SUBSET', subset, '#')
      # get runs from wandb
      try:
        wandb_project = WANDB_PROJECT.format(data=data, family=family.replace('/','_'), subset=subset)
        wandb_path = f'{WANDB_ENTITY}/{wandb_project}'
        print('Processing runs from', wandb_path)
        runs = wandb_api.runs(wandb_path)
        
        # iterate runs
        for run in runs:
          run_id = run.id
          name = run.name

          if ACTION == 'CLEAN':
            config = json.loads(run.json_config)
            # delete empty run
            if not config or run.state.lower() != 'finished':
              print('Deleting empty run', name, ', id:', run_id)
              run.delete()
          elif ACTION == 'CHECK_NAN':
            if name.startswith(PREFIX):
              run_files = run.files()
              
              for f in run_files:
                if f.name == 'output.log':
                  run_log = f
                  break

              log_txt = run_log.download(replace=True).read()
              if 'Monitored metric losses/val_loss = nan is not finite' in log_txt or 'loss=nan' in log_txt:
                  print('Nan loss detected:', name, ', id:', run_id)
          else:
            if name.startswith(PREFIX):
              if ACTION == 'DELETE':
                print('Deleting run', name, ', id:', run_id)
                # run.delete()
              elif ACTION == 'RENAME':
                print('Renaming run', name, ', id:', run_id)
                new_name = name.replace(PREFIX, NEW_PREFIX)
                print(name, '->', new_name)
                run.name = new_name
                run.update()
          
      except:
        print('Project not found:', wandb_project)
          

# # %%
# # RENAME RUN
# new_name = 'm6c19_baseline_s5'
# run_id = '27kqe0sy'
# run = wandb_api.run(f'cbe/kenn_figer_preliminary_tests_early_stop/{run_id}')
# run.name = new_name
# run.update()
# %%

# run = wandb_api.run(f'{WANDB_ENTITY}/{WANDB_PROJECT}/havgctl1'.format(data='figer', family='art', subset='10'))
# run
# %%
# name = run.name
# run_id = run.id
# if name.startswith(PREFIX):
#     run_files = run.files()
    
#     for f in run_files:
#       if f.name == 'output.log':
#         run_log = f
#         break

#     log_txt = run_log.download(replace=True).read()
#     if 'Monitored metric losses/val_loss = nan is not finite' in log_txt or 'loss=nan' in log_txt:
#       print('Nan loss detected:', name, ', id:', run_id)

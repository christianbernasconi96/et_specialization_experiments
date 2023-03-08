# %%
import wandb
import json 

wandb_api = wandb.Api()
WANDB_ENTITY = 'insides-lab-unimib-wandb'
WANDB_PROJECT = '{data}_specialization_{family}_subset{subset}'
ACTION = 'RENAME' # ['DELETE', 'RENAME']
PREFIX = 'box'
NEW_PREFIX = 'smart_init_box'
DATA=['figer', 'bbn']#, 'ontonotes_shimaoka']
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
  print()
  print('####### Data', data,'######')

  for family in FAMILY[data]:
    print()
    print('### FAMILY', family, '###')

    for subset in SUBSET:
      print()
      print('# SUBSET', subset, '#')
      # get runs from wandb
      wandb_project = WANDB_PROJECT.format(data=data, family=family.replace('/','_'), subset=subset)
      wandb_path = f'{WANDB_ENTITY}/{wandb_project}'
      print('Processing runs from', wandb_path)
      runs = wandb_api.runs(wandb_path)
      
      # iterate runs
      for run in runs:
        run_id = run.id
        name = run.name

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
        else:
          config = json.loads(run.json_config)
          # delete empty run
          if not config:
            print('Deleting empty run', name, ', id:', run_id)
            # run.delete()

# # %%
# # RENAME RUN
# new_name = 'm6c19_baseline_s5'
# run_id = '27kqe0sy'
# run = wandb_api.run(f'cbe/kenn_figer_preliminary_tests_early_stop/{run_id}')
# run.name = new_name
# run.update()
# %%

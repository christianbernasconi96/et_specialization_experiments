# %%
import os
import json
from tqdm import tqdm

DATA = 'few_NERD/supervised_formatted'
SRC_PATH = f'/home/remote_hdd/datasets/{DATA}/'
DST_PATH = f'/home/remote_hdd/datasets/{DATA}/only_fathers'
PARTITIONS = ['train', 'dev', 'test']

os.makedirs(DST_PATH, exist_ok=True)

for partition in PARTITIONS:
  print('Pruning types from', partition, '...')
  filename_src = os.path.join(SRC_PATH, f'{partition}.json')
  filename_dst = os.path.join(DST_PATH, f'{partition}.json')
  with open(filename_dst, 'w') as out:
    lines = open(filename_src, 'r').read().splitlines()
    for line in tqdm(lines):
      x = json.loads(line)
      x['y_str'] = ['/'.join(x['y_str'][0].split('/')[:-1])]
      out.write(json.dumps(x))
      out.write('\n')



# %%
import os
import pickle
import pandas as pd
from entity_typing_framework.main_module.inference_manager import IncrementalThresholdOrMaxInferenceManager
from entity_typing_framework.main_module.metric_manager import MetricManager, MetricManagerForIncrementalTypes
import entity_typing_framework.main_module.main_module as mm
import torch
from utils import forward_incremental

DATA=['figer', 'bbn']
DATA=['bbn']

PROJECTOR=['classifier', 'kenn_top_down', 'kenn_bottom_up', 'kenn_hybrid', 'box']
# PROJECTOR=['classifier']

TOKENIZER_CONFIG = {  
  'figer': 'bert-large-cased_M6L19R19T80_light.pickle',
  'bbn': 'bert-large-cased_M5L13R13T80_light.pickle'
}

MAIN_MODULE = {
  'classifier' : mm.IncrementalMainModule,
  'kenn_top_down' : mm.IncrementalKENNMultilossMainModule,
  'kenn_bottom_up' : mm.IncrementalKENNMultilossMainModule,
  'kenn_hybrid' : mm.IncrementalKENNMultilossMainModule,
  'box' : mm.IncrementalBoxEmbeddingMainModule
}

FAMILY = {
  'bbn' : [
    # 'CONTACT_INFO',
    #       'EVENT',
    #       'FACILITY',
    #       'GPE',
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
OUT_DIR_PATH = '../incremental/results/manual_test/{family}'
OUT_FILE = 'metrics_subset{subset}.csv'
DATA_PATH = '/home/remote_hdd/tokenized_datasets/{data}/specialization/incremental/{family}/subset_{subset}/instance_{instance}/{tokenizer_config}'

# %%

for data in DATA:
  for family in FAMILY[data]:
    # prepare out dir
    out_dir = OUT_DIR_PATH.format(family=family)
    os.makedirs(out_dir, exist_ok=True)
    # load test set
    # NOTE: the test set is shared across subsets and instances
    data_path = DATA_PATH.format(data=data, family=family, subset=SUBSET[0], instance=INSTANCE[0], tokenizer_config=TOKENIZER_CONFIG[data])
    tokenized_test = pickle.load(open(data_path, 'rb'))['tokenized_datasets']['test']
    tokenized_test_sentences = tokenized_test.tokenized_data['tokenized_sentences']
    input_ids = tokenized_test_sentences['input_ids']
    attention_mask = tokenized_test_sentences['attention_mask']
    one_hot_types = tokenized_test.tokenized_data['one_hot_types']


    for subset in SUBSET:
      # prepare output
      df = pd.DataFrame()
      out_file = OUT_FILE.format(subset=subset)
      out_file_path = os.path.join(out_dir, out_file)
      for projector in PROJECTOR:
        for instance in INSTANCE:
          # prepare model
          model_path = MODEL_PATH.format(data=data, family=family, subset=subset, instance=instance, model=projector)
          model = mm.IncrementalMainModule.load_ET_Network_for_test_(model_path).cuda()

          # prepare type utils
          type2id_pretrained = model.input_projector.pretrained_projector.type2id
          type2id_all = model.input_projector.additional_projector.type2id
          types_incremental = set(type2id_all.keys()) - set(type2id_pretrained.keys())
          type2id_incremental = { type_incremental : type2id_all[type_incremental] for type_incremental in types_incremental }
          type_number = len(type2id_all)
          fathers = set()
          for t in type2id_incremental.keys():
              f = t.replace(f"/{t.split('/')[-1]}", "")
              fathers.add(f)
          
          fathers = list(fathers)
          type2id_evaluation = { f : type2id_all[f] for f in fathers }
          type2id_evaluation.update(type2id_incremental)

          # prepare inference managers
          inference_manager = IncrementalThresholdOrMaxInferenceManager(name=None, threshold=.5, type2id=model.type2id)

          # prepare metric managers
          test_incremental_only_metric_manager = MetricManager(num_classes=len(type2id_incremental), device=model.device, prefix='test_incremental_only', type2id=type2id_incremental)
          test_incremental_only_exclusive_metric_manager = MetricManager(len(type2id_incremental), device=model.device, prefix='test_incremental_only', type2id=type2id_incremental)
          test_incremental_specific_metric_manager = MetricManagerForIncrementalTypes(type_number, device=model.device, prefix='test_incremental')
          # TODO: valutare altri metric managers... per me non servono

          # predict
          network_output_for_inference, y_true = forward_incremental(model, attention_mask, input_ids, one_hot_types, MAIN_MODULE[projector].get_output_for_inference)
          y_true = y_true.cuda()
          # infer types
          # network_output_for_inference = MAIN_MODULE[projector].get_output_for_inference(self=None, network_output=network_output)
          inferred_types = inference_manager.infer_types((network_output_for_inference[0].cuda(), network_output_for_inference[1].cuda()))

          # prepare metrics
          y_true = inference_manager.transform_true_types(y_true)
          # prepare filtered predictions with only incremental types
          idx = torch.tensor(list(type2id_incremental.values()))
          y_true_filtered = y_true.index_select(dim=1, index=idx.cuda())
          inferred_types_filtered = inferred_types.index_select(dim=1, index=idx.cuda())
          # update incremental only
          test_incremental_only_metric_manager.update(inferred_types_filtered.cuda(), y_true_filtered.cuda())
          # update metrics per type
          test_incremental_specific_metric_manager.update(inferred_types, y_true)
          # prepare filtered predictions with only incremental types and using only the examples that has at least one of the types of interes as true type 
          idx = torch.sum(y_true_filtered, dim=1).nonzero().squeeze()
          y_true_filtered = y_true_filtered.index_select(dim=0, index=idx.cuda())
          if torch.sum(y_true_filtered):
              inferred_types_filtered = inferred_types_filtered.index_select(dim=0, index=idx.cuda())
              # update incremental only exclusive
              test_incremental_only_exclusive_metric_manager.update(inferred_types_filtered, y_true_filtered)

          # compute metrics and aggregate
          test_incremental_only_exclusive_metrics = test_incremental_only_exclusive_metric_manager.compute()
          test_incremental_only_exclusive_metrics = {k.replace('macro_example', 'macro_example_exclusive'): v for k,v in test_incremental_only_exclusive_metrics.items() if 'macro_example' in k}
          test_incremental_specific_metrics = test_incremental_specific_metric_manager.compute(type2id_evaluation)
          test_incremental_only_metrics = test_incremental_only_metric_manager.compute()
          metrics = {}
          metrics.update(test_incremental_only_exclusive_metrics)
          metrics.update(test_incremental_specific_metrics)
          metrics.update(test_incremental_only_metrics)
          metrics = {k: v.cpu().item() for k, v in metrics.items()} 

          # compose df
          row = {'projector': projector, 'instance' : instance}
          row.update(metrics)
          if len(df) > 0:
            df = df.append(row, ignore_index=True)
          else:
            df = pd.DataFrame([row])

      # save csv
      df.to_csv(out_file_path, index=False)

# %%

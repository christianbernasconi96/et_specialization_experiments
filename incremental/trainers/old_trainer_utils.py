from tqdm import tqdm
import numpy as np

def calibrate_threshold(trainer, step=.025, metric='dev/macro_example/f1'):
  if trainer.model.inference_manager.calibrate_threshold:
      # compute patience as 10% of the total number of steps
      # patience = int(1000 // (step*1000) * .1)
      patience = 10
      counter = 0
      # disable validation metrics flag
      trainer.model.log_validation_metrics = False
      # iterate over thresholds and call validation routine
      max_metric = 0
      max_t = 0
      for t in tqdm(np.arange(step, 1, step), desc='Calibrating the threshold'):
          print()
          print('Validating model with threshold set to', t)
          trainer.model.inference_manager.threshold_incremental = t
          trainer.model.trainer.validate(trainer.model.trainer.model, trainer.model.trainer.datamodule.val_dataloader())
          current_metric = trainer.model.last_validation_metrics[metric]
          print()
          print(f'{metric}:', current_metric.item())
          if current_metric >= max_metric:
              print('Value improved')
              max_metric = current_metric
              max_t = t
              counter = 0
          else:
              print('Value not improved')
              counter += 1
              # early stop
              if counter == patience:
                print('*'*20)
                print(f'CALIBRATION WOULD STOP HERE, WITH THRESHOLD SET TO {max_t}')
                print('*'*20)
                break
      print('*'*20)
      print(f'Optimal threshold {max_t}')
      print('*'*20)
      # set optimal threshold
      trainer.model.inference_manager.threshold_incremental = max_t
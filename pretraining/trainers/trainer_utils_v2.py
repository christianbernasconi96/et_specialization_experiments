from tqdm import tqdm
import numpy as np

def calibrate_threshold(trainer, step=.025, metric='dev/macro_example/f1'):
    # TODO: move if to trainer.py
    if trainer.model.inference_manager.calibrate_threshold:
        # compute patience as 10% of the total number of steps
        patience = int(1000 // (step*1000) * .1)
        counter = 0
        # disable real validation routine
        trainer.model.prepare_threshold_calibration = True
        # aggregate network output of the validation set
        trainer.model.trainer.validate(trainer.model.trainer.model, trainer.model.trainer.datamodule.val_dataloader())
        network_output = trainer.model.trainer.network_output_for_calibration
        true_types = trainer.model.trainer.true_types_for_calibration
        
        # iterate over thresholds and compute metrics
        max_m = 0
        max_t = 0
        
        for t in tqdm(np.arange(step, 1, step), desc='Calibrating the threshold'):
            print()
            print('Validating model with threshold set to', t)
            # set new threshold
            trainer.model.inference_manager.threshold = t
            # infer types
            inferred_types = trainer.model.inference_manager.infer_types(network_output)
            # compute metrics
            trainer.model.metric_manager.update(inferred_types, true_types)
            metrics = trainer.model.metric_manager.compute()
            # check metric
            m = metrics[metric]
            print()
            print(f'{metric}:', m.item())
            if m > max_m:
                print('Value improved')
                max_m = m
                max_t = t
                counter = 0
            else:
                print('Value not improved')
                counter += 1
                # early stop
                if counter == patience:
                    break
        # set optimal threshold
        trainer.model.inference_manager.threshold = max_t

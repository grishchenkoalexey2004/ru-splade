import os

import torch

from splade.utils.utils import restore_model

# базовый класс для валидационных классов 
# отвечает за загрузку модели и ее перемещение на видеокарту!
class Evaluator:
    def __init__(self, model, config=None, restore=True):
        """
        :param model: model
        :param config: config dict
        :param restore: restore model true by default
        """
        self.model = model
        self.config = config
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        if restore: # если восстанавливаем модель по чекпоинту (а по дефолту у нас стоит true!)
            if self.device == torch.device("cuda"):
                if 'hf_training'  in config:
                    ## model already loaded
                    pass
                elif ("pretrained_no_yamlconfig" not in config or not config["pretrained_no_yamlconfig"] ):
                    checkpoint = torch.load(os.path.join(config["checkpoint_dir"], "model/model.tar"),
                                            map_location=self.device,weights_only=False)
                    restore_model(model, checkpoint["model_state_dict"])

                self.model.eval()
                if torch.cuda.device_count() > 1:
                    print(" --- use {} GPUs --- ".format(torch.cuda.device_count()))
                    self.model = torch.nn.DataParallel(self.model)
                self.model.to(self.device)
#                    print("restore model on GPU at {}".format(os.path.join(config["checkpoint_dir"], "model")),
#                        flush=True)
            else:  # CPU
                if 'hf_training'  in config:
                    ## model already loaded
                    pass                    
                elif ("pretrained_no_yamlconfig" not in config or not config["pretrained_no_yamlconfig"] ):
                    checkpoint = torch.load(os.path.join(config["checkpoint_dir"], "model/model.tar"),
                                            map_location=self.device,weights_only=False)
                    restore_model(model, checkpoint["model_state_dict"])
        else:
            print("WARNING: init evaluator, NOT restoring the model, NOT placing on device")
        self.model.eval()  # => put in eval mode

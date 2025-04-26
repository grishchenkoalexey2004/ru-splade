# данный модуль используется для построения индекса для коллекции документов 

import hydra
from omegaconf import DictConfig
import os

from conf.CONFIG_CHOICE import CONFIG_NAME, CONFIG_PATH
from .datasets.dataloaders import CollectionDataLoader
from .datasets.datasets import CollectionDatasetPreLoad
from .models.models_utils import get_model
from .tasks.transformer_evaluator import SparseIndexing
from .utils.utils import get_initialize_config

# просто индексация коллекции документов!
@hydra.main(config_path=CONFIG_PATH, config_name=CONFIG_NAME, version_base="1.2")
def index(exp_dict: DictConfig):
    exp_dict, config, init_dict, model_training_config = get_initialize_config(exp_dict)

    #if HF: need to udate config.
    if "hf_training" in config:
       init_dict.model_type_or_dir=os.path.join(config.checkpoint_dir,"model")
       init_dict.model_type_or_dir_q=os.path.join(config.checkpoint_dir,"model/query") if init_dict.model_type_or_dir_q else None
       print('HF model')

    # загрузка модели 
    model = get_model(config, init_dict)

    # инициализация dataloaderа для коллекции с документами 
    # exp_dict["data"]["COLLECTION_PATH"] лежит в конфигурационном файле для индекса!
    d_collection = CollectionDatasetPreLoad(data_dir=exp_dict["data"]["COLLECTION_PATH"], id_style="row_id")
    d_loader = CollectionDataLoader(dataset=d_collection, tokenizer_type=model_training_config["tokenizer_type"],
                                    max_length=model_training_config["max_length"],
                                    batch_size=config["index_retrieve_batch_size"],
                                    shuffle=False, num_workers=10, prefetch_factor=4)
    
    # построение разреженного обратного индекса с использованием hdf5
    evaluator = SparseIndexing(model=model, config=config, compute_stats=True)
    # постепенная индексация того, что у нас там лежит
    evaluator.index(d_loader)


if __name__ == "__main__":
    index()

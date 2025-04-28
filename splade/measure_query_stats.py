import time
from tqdm import tqdm
import hydra
from omegaconf import DictConfig
import torch
from conf.CONFIG_CHOICE import CONFIG_NAME, CONFIG_PATH
from .datasets.dataloaders import CollectionDataLoader
from .datasets.datasets import CollectionDatasetPreLoad
from .evaluate import evaluate
from .models.models_utils import get_model
from .tasks.transformer_evaluator import SparseRetrieval
from .utils.utils import get_dataset_name, get_initialize_config, restore_model
import os

# измеряет скорость генерации векторов для запросов 

@hydra.main(config_path=CONFIG_PATH, config_name=CONFIG_NAME, version_base="1.2")
def measure_query_stats(exp_dict: DictConfig):
    exp_dict, config, init_dict, model_training_config = get_initialize_config(exp_dict)

    # загрузка модели 
    model = get_model(config, init_dict)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    checkpoint = torch.load(os.path.join(config["checkpoint_dir"], "model/model.tar"),
                            map_location=device,weights_only=False)
    restore_model(model, checkpoint["model_state_dict"])


    batch_size = 32
    data_dir = exp_dict["data"]["Q_COLLECTION_PATH"][0]
  
    q_collection = CollectionDatasetPreLoad(data_dir=data_dir, id_style="row_id")
    q_loader = CollectionDataLoader(dataset=q_collection, tokenizer_type=model_training_config["tokenizer_type"],
                                        max_length=model_training_config["max_length"], batch_size=batch_size,
                                        shuffle=False, num_workers=4)
    
    
    start_time = time.time()
    
    for t, batch in enumerate(tqdm(q_loader)):
        # перекидываем output токенизатора на видеокарту (токенизатор всегда на cpu)
        inputs = {k: v.to(device) for k, v in batch.items() if k not in {"id"}}

        # генерация векторов моделью (в зависимости от того, что индексируется: документ или запрос)
        batch_documents = model(q_kwargs=inputs)["q_rep"]


    end_time = time.time()
    print(f"Time taken to process all queries: {end_time - start_time} seconds")
    print(f"Time taken per batch: {(end_time - start_time) / len(q_loader)} seconds")
    print(f"Time taken per query: {(end_time - start_time) / len(q_loader) / batch_size} seconds")


if __name__ == "__main__":
    measure_query_stats()
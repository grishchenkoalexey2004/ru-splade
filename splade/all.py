import hydra
from omegaconf import DictConfig

from conf.CONFIG_CHOICE import CONFIG_NAME, CONFIG_PATH
from .flops import flops
from .index import index
from .retrieve import retrieve_evaluate
from .train import train
from .utils.hydra import hydra_chdir
from .utils.index_figure import index_figure

# hydra отвечает за раскрытие полей заданных конфигурационных файлов!
@hydra.main(config_path=CONFIG_PATH, config_name=CONFIG_NAME)
def train_index_retrieve(exp_dict: DictConfig):
    # смена рабочей директории
    hydra_chdir(exp_dict)
    # обучение модели 
    train(exp_dict)
    # построение индекса (только для документов)
    index(exp_dict)
    # подсчёт метрик ранжирования
    retrieve_evaluate(exp_dict)
    # подсчёт метрики flops
    flops(exp_dict)
    
    index_figure(exp_dict)


if __name__ == "__main__":
    train_index_retrieve()

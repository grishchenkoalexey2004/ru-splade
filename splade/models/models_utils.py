from omegaconf import DictConfig

from ..models.transformer_rep import Splade, SpladeDoc, SpladeTopK, SpladeLexical


def get_model(config: DictConfig, init_dict: DictConfig):
    # no need to reload model here, it will be done later
    # (either in train.py or in Evaluator.__init__()

    model_map = {
        "splade": Splade,
        "splade_doc": SpladeDoc,
        "splade_topk": SpladeTopK,
        "splade_lexical": SpladeLexical
    }
    try:
        # узнает тип модели 
        model_class = model_map[config["matching_type"]]
    except KeyError:
        # не нашел тип модели 
        raise NotImplementedError("provide valid matching type ({})".format(config["matching_type"]))
    
    # инициализация модели с помощью параметров в init_dict
    return model_class(**init_dict)

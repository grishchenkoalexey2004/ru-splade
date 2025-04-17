import os

import hydra
from omegaconf import DictConfig
from transformers import AutoTokenizer, AutoModel
from huggingface_hub import HfApi
import torch
import os
from conf.CONFIG_CHOICE import CONFIG_NAME, CONFIG_PATH


@hydra.main(config_path=CONFIG_PATH, config_name=CONFIG_NAME, version_base="1.2")
def push_to_hf(exp_dict: DictConfig):
    

    # Get model checkpoint path from config
    checkpoint_path = exp_dict["checkpoint_dir"]
    
    if not os.path.exists(checkpoint_path):
        raise FileNotFoundError(f"Checkpoint not found at {checkpoint_path}")

    # Load the checkpoint
    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    
    # Get model config
    model_config = exp_dict["model"]
    
    # Initialize model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_config["model_type_or_dir"])
    model = AutoModel.from_pretrained(model_config["model_type_or_dir"])
    
    # Load state dict
    model.load_state_dict(checkpoint["model_state_dict"])
    
    # Get repository info from config
    repo_id = exp_dict["lesha-grishchenko"]
    
    # Push to Hub
    model.push_to_hub(repo_id)
    tokenizer.push_to_hub(repo_id)
    
    print(f"Model and tokenizer successfully pushed to {repo_id}")



if __name__ == "__main__":
    push_to_hf()
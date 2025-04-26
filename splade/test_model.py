import os
import sys
import hydra
import torch
from omegaconf import DictConfig


from transformers import AutoTokenizer
from .models.transformer_rep import Splade,SpladeDoc


# проверка базовой работоспособности модели на предложениях вводимых пользователем с клавиатуры
def test_model(checkpoint_dir, index_dir = None, out_dir = None):

    # перенос модели на cpu/gpu
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    if not os.path.exists(checkpoint_dir):
        print("Model not found!")
        exit(0)

    # определение типа модели 
    if "splade-doc" in checkpoint_dir:
        matching_type = "splade-doc"
    else:
        matching_type = "splade"

    model_dir = os.path.join(checkpoint_dir, "model")

    if matching_type == "splade-doc":
        model = SpladeDoc(model_dir, agg="max")
    elif matching_type == "splade":
        model = Splade(model_dir, agg="max")
    else:
        raise ValueError("Invalid matching type!")

    model.to(device)
    model.eval()

    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    reverse_voc = {v: k  for k, v in tokenizer.vocab.items()}

    while True:
        doc = input("Введите пример предложения: ")



        with torch.no_grad():
            tokens = tokenizer(doc, return_tensors="pt")
            tokens = tokens.to(device)

            doc_rep = model(d_kwargs=tokens)["d_rep"].squeeze()  # (sparse) doc rep in voc space, shape (30522,)

        # get the number of non-zero dimensions in the rep:
        col = torch.nonzero(doc_rep).squeeze().cpu().tolist()
        print("Количество ненулевых измерений: ", len(col))

        # now let's inspect the bow representation:
        weights = doc_rep[col].cpu().tolist()
        d = {k: v for k, v in zip(col, weights)}
        sorted_d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}
        bow_rep = []

        if "vk" in checkpoint_dir:
            for k, v in sorted_d.items():
                bow_rep.append((tokenizer.decode(k), round(v, 2)))
        else:
            for k, v in sorted_d.items():
                bow_rep.append((reverse_voc[k], round(v, 2)))

        print("Bag of words представление:\n", bow_rep)

        

if len(sys.argv) != 4:
    print("Error: Three arguments required")
    print("Usage: python -m splade.test_model <checkpoint_dir> <index_dir> <out_dir>")
    sys.exit(1)

checkpoint_dir = sys.argv[1]
index_dir = sys.argv[2] 
out_dir = sys.argv[3]

test_model(checkpoint_dir, index_dir, out_dir)
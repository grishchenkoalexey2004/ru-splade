import json
from datasets import load_from_disk
import random
import os


# скрипт предназначен для создания валидационного набора запросов и qrels

def load_qrels():
    qrels_path = "msmarco-ru/qrels/qrels.dev.json"
    with open(qrels_path) as f:
        qrels = json.load(f)
    return qrels


# для проверки того, что в qrels есть все запросы из dev (они действительно есть)
def get_dev_queries_ids():

    query_dev_dataset = load_from_disk("msmarco-ru/queries/dev")
        
    query_ids = set()
    for query in query_dev_dataset:
        query_ids.add(str(query["id"]))
        
    return query_ids


if __name__ == "__main__":


    qrels = load_qrels()

    # сохраняем часть qrels для валидации 
    val_qrels = dict() 


    query_dev_dataset = load_from_disk("msmarco-ru/queries/dev")


    # Get 500 random queries from the dataset
    random_indices = random.sample(range(len(query_dev_dataset)), 500)
    val_queries = query_dev_dataset.select(random_indices)


    # Create val directory if it doesn't exist
    os.makedirs("msmarco-ru/queries/val", exist_ok=True)

    # Save queries to TSV file
    with open("msmarco-ru/queries/val/queries.tsv", "w") as f:
        for query in val_queries:
            query_id = str(query["id"])
            val_qrels[query_id] = qrels[query_id]
            f.write(f"{query_id}\t{query['text']}\n")

    print(f"Saved {len(val_queries)} validation queries to msmarco-ru/queries/val/queries.tsv")


    json.dump(val_qrels, open("msmarco-ru/qrels/qrels.val.json", "w"))
    print(f"Saved {len(val_qrels)} validation qrels to msmarco-ru/qrels/qrels.val.json")

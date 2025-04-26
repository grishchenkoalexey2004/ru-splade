from tqdm import tqdm

import json 
import numpy as np 
import os 
import sys
# сокращает датасет коллекций до определенного количества документов! 
# выбирает все релевантные документы из qrels и добавляет неревантные документы из коллекции для того, чтобы общее количество документов было равно num_docs

# длина коллекции msmarco-passage!
COLLECTION_LEN = 8841823

def shrink_ds(qrels_path:str, collection_path:str, queries_path:str, num_docs:int, num_queries = None, collection_len = COLLECTION_LEN):

    if num_docs > collection_len:
        print("Ошибка: количество требуемых документов больше, чем количество документов в коллекции")
        exit(1)


    qrels = json.load(open(qrels_path))

    collection_dir = os.path.dirname(collection_path)
    
    query_ids = [] 
    query_texts = {}
    relevant_doc_ids = [] 

    with open(queries_path, 'r') as f:
        for line in f:
            query_id, query_text = line.split('\t')
            query_ids.append(query_id)
            query_texts[query_id] = query_text

    if num_queries == None:
        num_queries = len(query_ids)

    
    query_ids = np.random.choice(query_ids, size=num_queries, replace=False)

    # выбираем документы релевантные для выбранных запросов (если количество запросов не указано, то выбираем все запросы и все релевантные к ним документы!)
    with open(os.path.join(os.path.dirname(queries_path), f'shrinked_queries_{num_queries}.tsv'), 'w') as f_out:
        for query_id in query_ids:
            relevant_doc_ids.extend(list(qrels[query_id].keys()))
            f_out.write(f"{query_id}\t{query_texts[query_id]}")



    print(f"Для {num_queries} запросов найдено {len(relevant_doc_ids)} релевантных документов")

    if len(relevant_doc_ids) > num_docs:
        print("Количество релевантных документов больше, чем количество требуемых документов")
        print("Ошибка")
        exit(1)

    
    relevant_doc_ids = list(map(int, relevant_doc_ids))
    
    left_doc_ids = np.setdiff1d(np.arange(collection_len), relevant_doc_ids)

    left_doc_num = num_docs - len(relevant_doc_ids) 

    print(f"Выбираем из коллекции {len(relevant_doc_ids)} релевантных и {left_doc_num} нерелевантных документов")

    left_doc_ids = np.random.choice(left_doc_ids, size=left_doc_num, replace=False)


    included_rel_ids = [] 
    included_nonrel_ids = [] 

    with open(os.path.join(collection_dir, f'shrinked_collection_{num_docs}.tsv'), 'w') as f_out:
        with open(collection_path, 'r') as f_in:
            for line in tqdm(f_in, total=collection_len):
                doc_id = int(line.split('\t')[0])
                if doc_id in relevant_doc_ids:
                    f_out.write(line)
                    included_rel_ids.append(doc_id)
                if doc_id in left_doc_ids:
                    f_out.write(line)
                    included_nonrel_ids.append(doc_id)
                    

    
    print(f"Коллекция сохранена в {os.path.join(collection_dir, f'shrinked_collection_{num_docs}.tsv')}")

    # Find missing relevant docs
    missing_rel_ids = set(relevant_doc_ids) - set(included_rel_ids)
    if missing_rel_ids:
        print("\nМissing relevant document IDs:")
        print(sorted(list(missing_rel_ids)))
    else:
        print("\nAll relevant documents included successfully")

    # Find missing irrelevant docs 
    missing_nonrel_ids = set(left_doc_ids) - set(included_nonrel_ids)
    if missing_nonrel_ids:
        print("\nMissing non-relevant document IDs:")
        print(sorted(list(missing_nonrel_ids)))
    else:
        print("\nAll non-relevant documents included successfully")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Error: run_mode and doc_num must be specified")
        print("Usage: python shrink_ds.py <run_mode> <doc_num> [<query_num>]")
        exit(1)

    run_mode = sys.argv[1]
    num_docs = int(sys.argv[2])
    num_queries = int(sys.argv[3]) if len(sys.argv) > 3 else None


    if run_mode == None:
        print("Ошибка: не указан режим выполнения")
        exit(1) 


    print(f"Режим выполнения: {run_mode}")
    print(f"Количество требуемых документов: {num_docs}")
    print(f"Количество требуемых запросов: {num_queries}")

    if run_mode == "run":

        collection_path = "data/msmarco-ru/collection/collection.tsv"
        queries_path = "data/msmarco-ru/queries/dev/dev_queries.tsv"
        qrels_path = "data/msmarco-ru/qrels/dev_qrel.json"

        shrink_ds(qrels_path=qrels_path, collection_path=collection_path, queries_path=queries_path, num_docs=num_docs,num_queries=num_queries)

    elif run_mode == "debug":
        collection_len = 33
        collection_path = "data/full_collection/raw.tsv"
        queries_path = "data/dev_queries/raw.tsv"
        qrels_path = "data/dev_qrel.json"

        shrink_ds(qrels_path=qrels_path, collection_path=collection_path, queries_path=queries_path, num_docs=num_docs,num_queries=num_queries,collection_len=collection_len)

    else:
        print("Ошибка: неверный режим выполнения")
        exit(1)




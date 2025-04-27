from typing import Dict
from .bm25 import BM25Search

import json 
import argparse


from .evaluation import EvaluateRetrieval

HOSTNAME = "http://localhost:9200"
INDEX_NAME = "mmarco" 
LANGUAGE = "russian"
KEYS = {"body":"text"}



# данный скрипт преобразовывает tsv данные для работы с bm25 

# преобразование tsv файла к виду {query_id: query_text}
def query_to_bm25(query_file: str) -> Dict[str, str]:

    result = {}
    extracted_count = 0 

    with open(query_file, "r") as f:
        for line in f:
            query_id, query = line.split("\t")
            extracted_count += 1
            result[query_id] = query

    
    print(f"Extracted {extracted_count} queries from {query_file}")
    return result

# преобразование tsv файла к виду {doc_id : {text : document_text}}
def document_to_bm25(document_file: str) -> Dict[str, Dict[str, str]]:

    result = {}
    extracted_count = 0 

    with open(document_file, "r") as f:
        for line in f:
            doc_id, text = line.split("\t")
            extracted_count += 1
            result[doc_id] = {"text": text}

    print(f"Extracted {extracted_count} documents from {document_file}")
    return result

def load_qrels(qrels_file: str) -> Dict[str, Dict[str, int]]:
    with open(qrels_file, "r") as f:
        qrels = json.load(f)
        return qrels


def run_bm25(docs: Dict[str, Dict[str, str]], queries: Dict[str, str],qrels: Dict[str, Dict[str, int]], res_file: str) -> None:

    bm25 = BM25Search(index_name=INDEX_NAME, hostname=HOSTNAME, language=LANGUAGE, keys=KEYS)
    retriever = EvaluateRetrieval(bm25,k_values=[1000]) 

    results = retriever.retrieve(docs, queries)

    print("Successfulll retrieval, evaluating...")

    metrics = retriever.evaluate(qrels, results, k_values=[10,100,1000])
    specific_metrics = retriever.evaluate_custom(qrels, results, k_values=[10], metric="mrr")


    print(metrics)
    print(specific_metrics)

    with open(res_file, "w") as f:
        json.dump(metrics, f)
        json.dump(specific_metrics, f)

    return None 

"""
Main function to run BM25 retrieval and evaluation

Args:
    query_file: Path to queries TSV file
    document_file: Path to documents TSV file  
    qrels_file: Path to qrels JSON file
    res_file: Path to results JSON file
"""


parser = argparse.ArgumentParser()
parser.add_argument("query_file", help="Path to queries TSV file")
parser.add_argument("document_file", help="Path to documents TSV file")
parser.add_argument("qrels_file", help="Path to qrels JSON file") 
parser.add_argument("res_file", help="Path to results JSON file")
args = parser.parse_args()


# Load queries, documents and relevance judgments
queries = query_to_bm25(args.query_file)
docs = document_to_bm25(args.document_file)
qrels = load_qrels(args.qrels_file)


run_bm25(docs, queries, qrels, args.res_file)





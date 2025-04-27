# данный скрипт вычисляет метрики bm25 для сокращенной коллекции mmarco! 



from collections import Counter
from typing import Dict
from .bm25 import BM25Search

import json 
import argparse
import pytrec_eval
from pytrec_eval import RelevanceEvaluator





from .evaluation import EvaluateRetrieval

HOSTNAME = "http://localhost:9200"
INDEX_NAME = "mmarco" 
LANGUAGE = "russian"
KEYS = {"body":"text"}



def truncate_run(run, k):
    """truncates run file to only contain top-k results for each query"""
    temp_d = {}
    for q_id in run:
        sorted_run = {k: v for k, v in sorted(run[q_id].items(), key=lambda item: item[1], reverse=True)}
        temp_d[q_id] = {k: sorted_run[k] for k in list(sorted_run.keys())[:k]}
    return temp_d


def mrr_k(run, qrel, k, agg=True):
    evaluator = RelevanceEvaluator(qrel, {"recip_rank"})
    truncated = truncate_run(run, k)
    mrr = evaluator.evaluate(truncated)
    if agg:
        mrr = sum([d["recip_rank"] for d in mrr.values()]) / max(1, len(mrr))
    return mrr


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

    # metrics = retriever.evaluate(qrels, results, k_values=[10,100,1000])

    # specific_metrics = retriever.evaluate_custom(qrels, results, k_values=[10], metric="mrr")

    metric_dict = {}
    for k in [10,100,1000]:
        metrics = evaluate(results, qrels, "recall", agg=True, select=str(k))
        metric_dict["recall@{}".format(k)] = metrics
    

    mrr_10 = mrr_k(results, qrels, 10)
    metric_dict["mrr@10"] = mrr_10

    print("Полученные метрики: metric_dict = ", metric_dict)
    with open(res_file, "w") as f:
        json.dump(metric_dict, f)

    return None 


def evaluate(run, qrel, metric, agg=True, select=None):
    assert metric in pytrec_eval.supported_measures, print("provide valid pytrec_eval metric")
    evaluator = RelevanceEvaluator(qrel, {metric})
    out_eval = evaluator.evaluate(run)
    res = Counter({})
    if agg:
        for d in out_eval.values():  # when there are several results provided (e.g. several cut values)
            res += Counter(d)
        res = {k: v / len(out_eval) for k, v in res.items()}
        if select is not None:
            string_dict = "{}_{}".format(metric, select)
            if string_dict in res:
                return res[string_dict]
            else:  # If the metric is not on the dict, say that it was 0
                return 0
        else:
            return res
    else:
        return out_eval


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





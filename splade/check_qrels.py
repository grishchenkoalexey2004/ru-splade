# проверка того, что все запросы имеют релевантные документы, отмеченные в qrels

collection_path = "data/msmarco-ru/collection/collection.tsv"
queries_path = "data/msmarco-ru/queries/dev/dev_queries.tsv"
qrels_path = "data/msmarco-ru/qrels/dev_qrel.json"



import json
import pandas as pd

# Load qrels
with open(qrels_path, 'r') as f:
    qrels = json.load(f)

# Load queries
queries_df = pd.read_csv(queries_path, sep='\t', header=None, names=['id', 'text'])
query_ids = set(queries_df['id'].astype(str))

# Get qrels query IDs
qrels_query_ids = set(qrels.keys())

# Check for missing queries
missing_queries = query_ids - qrels_query_ids
if missing_queries:
    print("\nQueries missing from qrels:")
    print(sorted(list(missing_queries)))
else:
    print("\nAll queries have relevance judgments in qrels")

print(f"\nTotal queries: {len(query_ids)}")
print(f"Queries with qrels: {len(qrels_query_ids)}")

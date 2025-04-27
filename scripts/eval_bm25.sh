python -m bm25.bm25.msmarco_to_bm25 \
    data/msmarco-ru/queries/dev/dev_queries.tsv \
    data/msmarco-ru/collection/shrinked_collection_400000.tsv \
    data/msmarco-ru/qrels/dev_qrel.json \
    bm25/run.json


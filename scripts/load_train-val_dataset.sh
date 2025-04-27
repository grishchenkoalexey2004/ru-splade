


mkdir -p data/val_retrieval/collection
cd data/val_retrieval/collection

if [ ! -f raw.tsv ]; then
    wget https://huggingface.co/datasets/lesha-grishchenko/russian-ranking-triples/resolve/main/shrinked_collection_200000.tsv.gz
    gzip -d shrinked_collection_200000.tsv.gz
    mv shrinked_collection_200000.tsv raw.tsv
else
    echo "Collection already downloaded"
fi

cd ..




mkdir -p queries

cd queries

if [ ! -f raw.tsv ]; then
    wget https://huggingface.co/datasets/lesha-grishchenko/russian-ranking-triples/resolve/main/shrinked_queries_500.tsv
    mv shrinked_queries_500.tsv raw.tsv
else
    echo "Shrinked queries already downloaded"
fi

cd ../..

if [ ! -f dev_qrel.json ]; then
    wget https://huggingface.co/datasets/lesha-grishchenko/russian-ranking-triples/resolve/main/dev_qrel.json
else
    echo "Dev qrel already downloaded"
fi

# loading collection 


mkdir -p data/full_collection
cd data/full_collection

if [ ! -f raw.tsv ]; then
    wget https://huggingface.co/datasets/lesha-grishchenko/russian-ranking-triples/resolve/main/collection.tsv.gz
    gzip -d collection.tsv.gz
    mv collection.tsv raw.tsv
else
    echo "Collection already downloaded"
fi

cd ../../



mkdir -p data/dev_queries 

cd data/dev_queries 

if [ ! -f raw.tsv ]; then
    wget https://huggingface.co/datasets/lesha-grishchenko/russian-ranking-triples/resolve/main/dev_queries.tsv
    mv dev_queries.tsv raw.tsv
else
    echo "Dev queries already downloaded"
fi

cd ..

if [ ! -f dev_qrel.json ]; then
    wget https://huggingface.co/datasets/lesha-grishchenko/russian-ranking-triples/resolve/main/qrels.dev.json
    mv qrels.dev.json dev_qrel.json
else
    echo "Dev qrel already downloaded"
fi








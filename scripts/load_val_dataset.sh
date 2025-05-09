# загрузка датасета для финальной валидации модели! 


mkdir -p data/full_collection
cd data/full_collection

if [ ! -f raw.tsv ]; then
    wget https://huggingface.co/datasets/lesha-grishchenko/russian-ranking-triples/resolve/main/shrinked_collection_400000.tsv.gz
    gzip -d shrinked_collection_400000.tsv.gz
    mv shrinked_collection_400000.tsv raw.tsv
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
    wget https://huggingface.co/datasets/lesha-grishchenko/russian-ranking-triples/resolve/main/dev_qrel.json
else
    echo "Dev qrel already downloaded"
fi








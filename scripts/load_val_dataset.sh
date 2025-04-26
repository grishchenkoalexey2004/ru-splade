# loading collection 


mkdir -p data/full_collection
cd data/full_collection

if [ ! -f raw.tsv ]; then
    wget https://huggingface.co/datasets/lesha-grishchenko/russian-ranking-triples/resolve/main/collection.tsv.gz?download=true
    gzip -d collection.tsv.gz
    mv collection.tsv raw.tsv
fi

else
    echo "Collection already downloaded"
fi

cd ../../



mkdir -p data/dev_queries 

cd data/dev_queries 

if [ ! -f raw.tsv ]; then
    wget https://huggingface.co/datasets/lesha-grishchenko/russian-ranking-triples/resolve/main/dev_queries.tsv?download=true
    mv dev_queries.tsv raw.tsv
fi

else
    echo "Dev queries already downloaded"
fi

cd ..

if [ ! -f dev_qrel.json ]; then
    wget https://huggingface.co/datasets/lesha-grishchenko/russian-ranking-triples/resolve/main/qrels.dev.json?download=true
    mv qrels.dev.json dev_qrel.json
fi
    
else
    echo "Dev qrel already downloaded"
fi








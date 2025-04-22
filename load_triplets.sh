mkdir -p data
cd data

wget -q https://huggingface.co/datasets/lesha-grishchenko/russian-ranking-triples/resolve/main/chunk_1.tsv.gz

tar -xzvf chunk_1.tsv.gz
mv chunk_1.tsv raw.tsv
rm -r chunk_1.tsv.gz
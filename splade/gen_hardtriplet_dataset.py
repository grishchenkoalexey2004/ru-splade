from tqdm import tqdm
NUM_TRIPLETS = 3500000



triplet_ids_dir = "data/hard-triplets/hard-triplets.tsv"
query_dir = "data/hard-triplets/train_dqueries.tsv"
collection_dir = "data/full_collection/collection.tsv"

result_file = "data/hard-triplets/raw.tsv"


# Create dictionaries to store queries and documents
queries = {}
documents = {}

# Load queries
with open(query_dir, 'r', encoding='utf-8') as f:
    for line in f:
        qid, query = line.strip().split('\t')
        queries[qid] = query

# Load documents
with open(collection_dir, 'r', encoding='utf-8') as f:
    for line in f:
        did, doc = line.strip().split('\t')
        documents[did] = doc


with open(result_file, 'w', encoding='utf-8') as f_out:
    with open(triplet_ids_dir, 'r', encoding='utf-8') as f:
        for i, line in enumerate(tqdm(f, total=NUM_TRIPLETS)):
            if i >= NUM_TRIPLETS:
                break
            qid, pos_did, neg_did = line.strip().split('\t')
            result_line = f"{queries[qid]}\t{documents[pos_did]}\t{documents[neg_did]}\n"
            f_out.write(result_line)





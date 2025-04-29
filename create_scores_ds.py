# 
# 
# 
# 
# 
# 
import pickle
from tqdm import tqdm
import json
import os



#       self.query_list = list()
#         for query in query_list:
#             if str(query) in self.qrels.keys():
#                 self.query_list.append(query)
#         print("QUERY SIZE = ", len(self.query_list))

#     def __len__(self):
#         return len(self.query_list)

#     # короче возвращает триплеты (query, doc_pos, doc_neg, score_pos, score_neg)
#     def __getitem__(self, idx):
#         query = self.query_list[idx]
#         q = self.query_dataset[str(query)][1]
#         candidates_dict = self.scores_dict[query]
#         candidates = list(candidates_dict.keys())
#         # positives - список id документов реально релевантных запросу
#         positives = list(self.qrels[str(query)].keys())
#         # удаляем из списка кандидатов документы, которые действительно релевантны запросу (остаются negatives)
#         for positive in positives:
#             candidates.remove(int(positive))
#         # выбираем рандомный документ из списка положительных и вычисляем его score
#         positive = random.sample(positives, 1)[0]
#         s_pos = candidates_dict[int(positive)]
#         # в списке candidates остались только отрицательные документы (берем случайный и генерируем его score)
#         negative = random.sample(candidates, 1)[0]
#         s_neg = candidates_dict[negative]
#         # получаем документы
#         d_pos = self.document_dataset[positive][1]
#         d_neg = self.document_dataset[str(negative)][1]


pickle_path = "data/scores.pkl"

with open(pickle_path, "rb") as fIn:
    scores_dict = pickle.load(fIn)

print("loaded pickle!")


triplet_ids_dir = "data/hard-triplet-ids/hard-triplet-ids.tsv"
query_dir = "data/queries/train-queries.tsv"
collection_dir = "data/collection/collection.tsv"
qrels_dir = "data/train_qrel.json"



result_file = "data/fives/raw.tsv"
os.makedirs(os.path.dirname(result_file), exist_ok=True)


# Create dictionaries to store queries and documents
queries = {}
documents = {}
qrels = json.load(open(qrels_dir, 'r', encoding='utf-8'))

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
    with open(triplet_ids_dir, 'r', encoding='utf-8') as f_in:
        for i, line in enumerate(tqdm(f_in)):
            qid, pos_did, neg_did = map(int, line.strip().split('\t'))
            pos_doc = documents[str(pos_did)]
            neg_doc = documents[str(neg_did)]
            query_doc = queries[str(qid)]

            if str(qid) in qrels and qid in scores_dict:
                s_pos = scores_dict[qid][pos_did]
                s_neg = scores_dict[qid][neg_did]
                
                f_out.write(f"{query_doc}\t{pos_doc}\t{neg_doc}\t{s_pos}\t{s_neg}\n")



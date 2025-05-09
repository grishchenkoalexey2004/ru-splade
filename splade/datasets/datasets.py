import gzip
import json
import os
import pickle
import random
from torch.utils.data import Dataset
from tqdm.auto import tqdm


# загрузчик триплетов
class PairsDatasetPreLoad(Dataset):
    """
    dataset to iterate over a collection of pairs, format per line: q \t d_pos \t d_neg
    we preload everything in memory at init
    """

    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.id_style = "row_id"
        self.deleted_count = 0 
        self.index = 0 
        # словарь номер_строки -> (query, doc_pos, doc_neg)
        self.data_dict = {}  # => dict that maps the id to the line offset (position of pointer in the file)
        print("Preloading dataset")
        self.data_dir = os.path.join(self.data_dir, "raw.tsv")
        with open(self.data_dir) as reader:
            for line in tqdm(reader):
                if len(line) > 1:
                    query, pos, neg = line.split("\t")  # first column is id
                    if "Â" in query or "Â" in pos or "Â" in neg: 
                        self.deleted_count += 1
                    else:
                        self.data_dict[self.index] = (query.strip(), pos.strip(), neg.strip())
                        self.index += 1 

        # количество экземпляров    
        self.nb_ex = len(self.data_dict)
        print(f"Удалено дефектных триплетов: {self.deleted_count}")
        print(f"Загружено триплетов: {self.nb_ex}")

    # возврат количества экземплятров в файле
    def __len__(self):
        return self.nb_ex

    # возврат 
    def __getitem__(self, idx):
        return self.data_dict[idx]


class DistilPairsDatasetPreLoad(Dataset):
    """
    dataset to iterate over a collection of pairs, format per line: q \t d_pos \t d_neg \t s_pos \t s_neg
    we preload everything in memory at init
    """

    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.id_style = "row_id"
        self.data_dict = {}  # => dict that maps the id to the line offset (position of pointer in the file)
        print("Preloading dataset")
        self.data_dir = os.path.join(self.data_dir, "raw.tsv")
        self.deleted_count = 0
        self.index = 0
        with open(self.data_dir) as reader:
            for line in tqdm(reader):
                if len(line) > 1:
                    q, d_pos, d_neg, s_pos, s_neg = line.split("\t")
                    if "Â" in q or "Â" in d_pos or "Â" in d_neg: 
                        self.deleted_count += 1
                    else:
                        self.data_dict[self.index] = (
                            q.strip(), d_pos.strip(), d_neg.strip(), float(s_pos.strip()), float(s_neg.strip()))
                        self.index += 1
        
        self.nb_ex = len(self.data_dict)

        print(f"Удалено дефектных триплетов: {self.deleted_count}")
        print(f"Загружено триплетов: {self.nb_ex}")
        

    def __len__(self):
        return self.nb_ex

    def __getitem__(self, idx):
        return self.data_dict[idx]

# загрузка документов или query 
# все операции такие же как и для триплетов!
class CollectionDatasetPreLoad(Dataset):
    """
    dataset to iterate over a document/query collection, format per line: format per line: doc_id \t doc
    we preload everything in memory at init
    """

    def __init__(self, data_dir, id_style):
        self.data_dir = data_dir
        assert id_style in ("row_id", "content_id"), "provide valid id_style"
        # id_style indicates how we access the doc/q (row id or doc/q id)
        self.id_style = id_style
        self.data_dict = {}
        self.line_dict = {}
        print("Preloading dataset")
        with open(os.path.join(self.data_dir, "raw.tsv")) as reader:
            for i, line in enumerate(tqdm(reader)):
                if len(line) > 1:
                    id_, *data = line.split("\t")  # first column is id
                    # убирает табуляции и \n из текстов документов
                    data = " ".join(" ".join(data).splitlines())
                    
                    # нумерация пар по номеру строки
                    if self.id_style == "row_id":
                        self.data_dict[i] = data # словарь номер_строки -> информация
                        self.line_dict[i] = id_.strip() # словарь номер строки -> _id query в триплете
                    else:
                        # нумерация по id запроса
                        self.data_dict[id_] = data.strip()

        # длина датасета
        self.nb_ex = len(self.data_dict)

    def __len__(self):
        return self.nb_ex

    # получение доступа к элементам датасета через номер строки (id_style = row_id) или qid 
    def __getitem__(self, idx):
        if self.id_style == "row_id":
            # за счёт номера строки получаем qid, и документы
            return self.line_dict[idx], self.data_dict[idx]
        else:
            return str(idx), self.data_dict[str(idx)]


class BeirDataset(Dataset):
    """
    dataset to iterate over a BEIR collection
    we preload everything in memory at init

    работает также и для rusbeir! 
    """

    def __init__(self, value_dictionary, information_type="document"):
        assert information_type in ["document", "query"]
        self.value_dictionary = value_dictionary
        self.information_type = information_type
        if self.information_type == "document":
            self.value_dictionary = dict()
            for key, value in value_dictionary.items():
                self.value_dictionary[key] = value["title"] + " " + value["text"]
        self.idx_to_key = {idx: key for idx, key in enumerate(self.value_dictionary)}

    def __len__(self):
        return len(self.value_dictionary)

    def __getitem__(self, idx):
        true_idx = self.idx_to_key[idx]
        return idx, self.value_dictionary[true_idx]
    



class MsMarcoHardNegatives(Dataset):
    """
    class used to work with the hard-negatives dataset from sentence transformers
    see: https://huggingface.co/datasets/sentence-transformers/msmarco-hard-negatives
    """

    def __init__(self, dataset_path, document_dir, query_dir, qrels_path):
        self.document_dataset = CollectionDatasetPreLoad(document_dir, id_style="content_id")
        self.query_dataset = CollectionDatasetPreLoad(query_dir, id_style="content_id")
        with gzip.open(dataset_path, "rb") as fIn:
            self.scores_dict = pickle.load(fIn)
        query_list = list(self.scores_dict.keys())
        with open(qrels_path) as reader:
            self.qrels = json.load(reader)
        self.query_list = list()
        # добавляет все запросы, которые есть в pkl
        for query in query_list:
            if str(query) in self.qrels.keys():
                self.query_list.append(query)
        print("QUERY SIZE = ", len(self.query_list))

    def __len__(self):
        return len(self.query_list)

    # короче возвращает триплеты (query, doc_pos, doc_neg, score_pos, score_neg)
    def __getitem__(self, idx):
        query = self.query_list[idx]
        q = self.query_dataset[str(query)][1]
        candidates_dict = self.scores_dict[query]
        candidates = list(candidates_dict.keys())
        # positives - список id документов реально релевантных запросу
        positives = list(self.qrels[str(query)].keys())
        # удаляем из списка кандидатов документы, которые действительно релевантны запросу (остаются negatives)
        for positive in positives:
            candidates.remove(int(positive))
        # выбираем рандомный документ из списка положительных и вычисляем его score
        positive = random.sample(positives, 1)[0]
        s_pos = candidates_dict[int(positive)]
        # в списке candidates остались только отрицательные документы (берем случайный и генерируем его score)
        negative = random.sample(candidates, 1)[0]
        s_neg = candidates_dict[negative]
        # получаем документы
        d_pos = self.document_dataset[positive][1]
        d_neg = self.document_dataset[str(negative)][1]
        # возвращаем пятерку (query, positive_doc, negative_doc, positive_score, negative_score)
        return q.strip(), d_pos.strip(), d_neg.strip(), float(s_pos), float(s_neg)



class IR_Dataset(Dataset):
    """
    dataset to iterate over a document/query collection, receives a dictionary id, text
    """

    def __init__(self, ir_dataset, information_type="document", sequential_idx=True, all_docs=None):
        assert information_type in ["document", "query"]
        self.ir_dataset = ir_dataset
        
        self.information_type = information_type
        self.value_dictionary = dict()
        self.key_to_id = dict()
        self.sequential_idx = sequential_idx
        self.all_docs = all_docs

        # We use the natural order of query/document as key, because ids of the different beir datasets
        # have different types (str vs int) which is problematic with FAISS index.
        if self.information_type == "document":
            for idx, value in enumerate(tqdm(ir_dataset.docs_iter())):
                if not sequential_idx:
                    idx = value.doc_id
                    if all_docs:
                        if idx not in all_docs:
                            continue
                    idx = value.doc_id.replace('"',"")

                try:
                    self.value_dictionary[idx] = value.title+" "+value.text
                except:
                    try:
                        self.value_dictionary[idx] = value.body.decode('iso-8859-1')+" "+value.url
                    except:
                        self.value_dictionary[idx] = value.text
                self.key_to_id[idx] = value.doc_id
        if self.information_type == "query":
            for idx, value in enumerate(ir_dataset.queries_iter()):
                if not sequential_idx:
                    idx = value.query_id
                self.value_dictionary[idx] = value.text
                self.key_to_id[idx] = value.query_id

    def __len__(self):
        return len(self.value_dictionary)

    def __getitem__(self, idx):
        return idx, self.value_dictionary[idx]
    
class IR_Dataset_NoLoad(Dataset):
    """
    dataset to iterate over a document/query collection, receives a dictionary id, text
    """

    def __init__(self, ir_dataset):
        self.ir_dataset = ir_dataset
        self.docs_store = ir_dataset.docs_store()
        all_decoded = dict()

    def __len__(self):
        return len(self.value_dictionary)

    def __getitem__(self, idx):
        value = self.docs_store.get(idx)
        text = ""
        try: 
            text = value.title+" "+value.text
        except:
            try:
                text = value.body.decode('iso-8859-1')+" "+value.url
            except:
                text = value.text
        return idx, text


if __name__ == "__main__":
    pairs_dataset = PairsDatasetPreLoad("test-data-triplets")
    print(pairs_dataset.data_dict)


    
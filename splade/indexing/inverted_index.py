"""
code for inverted index based on arrays, powered by numba based retrieval
"""

import array
import json
import os
import pickle
from collections import defaultdict

import h5py
import numpy as np
from tqdm.auto import tqdm


class IndexDictOfArray:
    def __init__(self, index_path=None, force_new=False, filename="array_index.h5py", dim_voc=None):

        """
        Индекс по сути устроен так: 

        есть словарь токен -> массив из id документов в которых он встречается 
        есть словарь токен -> массив float значений соответствующих токену в этих документах 

        все это хранится с помощью оптимизаций numpy, array и h5py 
        numpy - для распаковки из h5py формата
        h5py - для хранения 


        в файле h5py для i-ого токена (i in [0, dim_voc)) хранится 2 массива (датасета):
        index_doc_id_i - массив id документов где встречается i-ый токен
        index_doc_value_i - массив значений i-ого токена в этих документах
        """
        if index_path is not None:
            # создание директории под индекс    
            self.index_path = index_path
            if not os.path.exists(index_path):
                os.makedirs(index_path)
            # имя файла под индекс
            self.filename = os.path.join(self.index_path, filename)
            # если файл существует и не нужно создавать новый, то загружаем индекс
            if os.path.exists(self.filename) and not force_new:
                print("index    already exists, loading...")
                # создание объекта файла для чтения ранее созданного индекса
                self.file = h5py.File(self.filename, "r")
                if dim_voc is not None:
                    dim = dim_voc
                else:
                    dim = self.file["dim"][()]
                self.index_doc_id = dict() # словарь для хранения id документов
                self.index_doc_value = dict() # словарь для хранения векторов документов

                # для каждого токена из словаря
                for key in tqdm(range(dim)):
                    try:
                        # распаковка токен -> id документов где он встречается
                        self.index_doc_id[key] = np.array(self.file["index_doc_id_{}".format(key)],
                                                          dtype=np.int32)
                        # распаковка токен -> вектор значений токена в документах
                        # ideally we would not convert to np.array() but we cannot give pool an object with hdf5
                        self.index_doc_value[key] = np.array(self.file["index_doc_value_{}".format(key)],
                                                             dtype=np.float32)
                    except:
                        self.index_doc_id[key] = np.array([], dtype=np.int32)
                        self.index_doc_value[key] = np.array([], dtype=np.float32)
                self.file.close()
                del self.file
                print("done loading index...")
                # загрузка массива id документов из pickle файла
                doc_ids = pickle.load(open(os.path.join(self.index_path, "doc_ids.pkl"), "rb"))
                self.n = len(doc_ids)
            else:
                # инициализация нового индекса если необходимо его обновить!
                self.n = 0
                print("initializing new index...")
                # array библиотека используется для оптимизации хранения массивов однородных данных 
                # тип данных в такой структуре утановлен и не может быть другим 
                self.index_doc_id = defaultdict(lambda: array.array("I")) # I - unsigned int32 
                self.index_doc_value = defaultdict(lambda: array.array("f")) # f - float32
        else:
            # инициализация нового индекса (если нет пути к индексу)
            self.n = 0
            print("initializing new index...")
            self.index_doc_id = defaultdict(lambda: array.array("I"))
            self.index_doc_value = defaultdict(lambda: array.array("f"))

    def add_batch_document(self, row, col, data, n_docs=-1):
        """add a batch of documents to the index
        """
        # увеличение счетчика количества документов в индексе
        if n_docs < 0:
            self.n += len(set(row))
        else:
            self.n += n_docs

        # 
        for doc_id, dim_id, value in zip(row, col, data):
            self.index_doc_id[dim_id].append(doc_id)
            self.index_doc_value[dim_id].append(value)

    def __len__(self):
        return len(self.index_doc_id)

    def nb_docs(self):
        return self.n

    def save(self, dim=None):
        print("converting to numpy")

        # преобразование массивов из array в numpy (по-другому нельзя загрузить в h5py)
        for key in tqdm(list(self.index_doc_id.keys())):
            self.index_doc_id[key] = np.array(self.index_doc_id[key], dtype=np.int32)
            self.index_doc_value[key] = np.array(self.index_doc_value[key], dtype=np.float32)
        print("save to disk")
        with h5py.File(self.filename, "w") as f:
            if dim:
                # информация о размерности индекса
                f.create_dataset("dim", data=int(dim))
            else:
                # информация о размерности индекса (если она изначально не была задана) 
                # может оказаться так, что некоторые токены токенизатора не встречаются в индексе
                f.create_dataset("dim", data=len(self.index_doc_id.keys()))
            for key in tqdm(self.index_doc_id.keys()):
                # создание двух датасетов для каждого токена: tok -> doc_id и tok->doc_value
                f.create_dataset("index_doc_id_{}".format(key), data=self.index_doc_id[key])
                f.create_dataset("index_doc_value_{}".format(key), data=self.index_doc_value[key])
            f.close()
        print("saving index distribution...")  # => size of each posting list in a dict
        # распределение для индекса 
        # показывает распределение количества документов для каждого токена
        index_dist = {}
        for k, v in self.index_doc_id.items():
            index_dist[int(k)] = len(v)
        json.dump(index_dist, open(os.path.join(self.index_path, "index_dist.json"), "w"))


        # сюды можно еще какие-нибудь метрики добавить

# загрузка всех необходимых для обучения датасетов:
from datasets import load_dataset


dataset = load_dataset('unicamp-dl/mmarco', 'russian')
dataset.save_to_disk("msmarco-ru/triplets")


dataset = load_dataset('unicamp-dl/mmarco', 'queries-russian')
dataset.save_to_disk("msmarco-ru/queries")

dataset = load_dataset('unicamp-dl/mmarco', 'collection-russian')
dataset.save_to_disk('msmarco-ru')



# загрузка всех необходимых для обучения датасетов:
from datasets import load_dataset
try:
    dataset = load_dataset('unicamp-dl/mmarco', 'russian')
    dataset.save_to_disk("msmarco-ru/triplets")
except Exception as e:
    print(f"Error downloading/saving triplets dataset: {e}")

try:
    dataset = load_dataset('unicamp-dl/mmarco', 'queries-russian') 
    dataset.save_to_disk("msmarco-ru/queries")
except Exception as e:
    print(f"Error downloading/saving queries dataset: {e}")

try:
    dataset = load_dataset('unicamp-dl/mmarco', 'collection-russian')
    dataset.save_to_disk('msmarco-ru')
except Exception as e:
    print(f"Error downloading/saving collection dataset: {e}")

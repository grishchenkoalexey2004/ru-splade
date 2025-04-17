from datasets import load_dataset
import os


pyarrow_chunk_name = "msmarco-ru/triplets/train/data-00112-of-00113.arrow"

# Load the dataset from parquet format
dataset = load_dataset("arrow", data_files=pyarrow_chunk_name)["train"]

# Convert to TSV format
output_file = "msmarco-ru/triplets/train/raw.tsv"

with open(output_file, "w", encoding="utf-8") as f:
    
    
    # Write data rows
    for row in dataset:
        values = [str(row[col]) for col in dataset.column_names]
        f.write("\t".join(values) + "\n")

print(f"Converted arrow file to TSV at {os.path.abspath(output_file)}")

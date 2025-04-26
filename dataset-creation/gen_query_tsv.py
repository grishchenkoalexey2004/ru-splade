import json
from datasets import load_from_disk
import os

def convert_queries_to_tsv(input_path, output_path):
    """
    Convert queries from Arrow/Parquet format to TSV format
    Args:
        input_path: Path to the input queries in Arrow/Parquet format
        output_path: Path to save the output TSV file
    """
    # Load queries dataset
    dataset = load_from_disk(input_path)
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write queries to TSV file
    with open(output_path, "w", encoding="utf-8") as f:
        for query in dataset:
            print(query)
            # Write query ID and text separated by tab
            f.write(f"{query['id']}\t{query['text']}\n")

if __name__ == "__main__":
    # Convert dev queries
    convert_queries_to_tsv(
        "msmarco-ru/queries/dev",
        "msmarco-ru/queries/dev/dev_queries.tsv"
    )

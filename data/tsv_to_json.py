import json
from collections import defaultdict

def tsv_to_json(tsv_file, json_file):
    """
    Convert TSV file with query_id, doc_id, score to JSON format
    where key is query_id and value is list of relevant doc_ids
    """
    # Dictionary to store query_id -> list of doc_ids
    query_docs = defaultdict(dict)
    
    # Read TSV file
    with open(tsv_file, 'r') as f:
        for line in f:
            # Split line by tab
            query_id, _, doc_id, score = line.strip().split('\t')
            # Add doc_id to the list for this query_id
            query_docs[query_id].update({doc_id:score})
    
    # Write to JSON file
    with open(json_file, 'w') as f:
        json.dump(query_docs, f, indent=2)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert TSV to JSON format')
    parser.add_argument('--tsv', required=True, help='Input TSV file path')
    parser.add_argument('--json', required=True, help='Output JSON file path')
    
    args = parser.parse_args()
    
    tsv_to_json(args.tsv, args.json)
    print(f"Conversion complete. Output written to {args.json}")    
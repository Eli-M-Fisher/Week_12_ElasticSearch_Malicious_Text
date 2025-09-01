import pandas as pd
from app.elastic_client import get_client, create_index_if_missing
from app.config import ELASTIC_INDEX

# load CSV data into Elasticsearch
def load_csv_to_elastic(csv_path: str):
    client = get_client()
    create_index_if_missing(client)

    df = pd.read_csv(csv_path)

    # Fix TweetID issues


        # Iterate and index


    print(f"Indexed {len(df)} documents into {ELASTIC_INDEX}")
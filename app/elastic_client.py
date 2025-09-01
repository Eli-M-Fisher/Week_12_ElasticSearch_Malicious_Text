# module to handle Elasticsearch client and index creation
import time
from elasticsearch import Elasticsearch
from app.config import ELASTIC_HOST, ELASTIC_INDEX, INDEX_MAPPING

# here i get Elasticsearch client
def get_client():
    print(f"Connecting to Elasticsearch at {ELASTIC_HOST}")
    return Elasticsearch(ELASTIC_HOST)

# and create index if it doesn't exist
# with retries to handle ES startup delay
def create_index_if_missing(client, retries: int = 12):
    for i in range(retries):
        try:
            if not client.indices.exists(index=ELASTIC_INDEX):
                client.indices.create(index=ELASTIC_INDEX, body=INDEX_MAPPING)
            return
        except Exception as e:
            print(f"Elasticsearch not ready yet ({i+1}/{retries}). Retrying...")
            time.sleep(5)
    raise RuntimeError("Elasticsearch is not reachable after retries")
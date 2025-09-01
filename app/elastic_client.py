# module to handle Elasticsearch client and index creation
from elasticsearch import Elasticsearch
from app.config import ELASTIC_HOST, ELASTIC_INDEX, INDEX_MAPPING

# here i get Elasticsearch client
def get_client():
    return Elasticsearch(ELASTIC_HOST)

# and create index if it doesn't exist
def create_index_if_missing(client):
    if not client.indices.exists(index=ELASTIC_INDEX):
        client.indices.create(index=ELASTIC_INDEX, body=INDEX_MAPPING)
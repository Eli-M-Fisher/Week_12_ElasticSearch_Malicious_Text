from fastapi import APIRouter
from elasticsearch import Elasticsearch
from app.elastic_client import get_client
from app.config import ELASTIC_INDEX
import app.config as config

router = APIRouter()

@router.get("/antisemitic-weapons")
def get_antisemitic_with_weapons():
    if not config.PROCESSING_DONE:
        return {"message": "Data not processed yet."}

    client: Elasticsearch = get_client()
    query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"Antisemitic": 1}},
                    {"script": {"script": "doc['weapons'].size() > 0"}},
                ]
            }
        }
    }
    resp = client.search(index=ELASTIC_INDEX, body=query, size=1000)
    docs = [hit["_source"] for hit in resp["hits"]["hits"]]
    return {"results": docs}

@router.get("/multi-weapons")
def get_with_multiple_weapons():
    if not config.PROCESSING_DONE:
        return {"message": "Data not processed yet."}

    client: Elasticsearch = get_client()
    query = {
        "query": {
            "script": {
                "script": "doc['weapons'].size() >= 2"
            }
        }
    }
    resp = client.search(index=ELASTIC_INDEX, body=query, size=1000)
    docs = [hit["_source"] for hit in resp["hits"]["hits"]]
    return {"results": docs}

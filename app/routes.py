from fastapi import APIRouter
from elasticsearch import Elasticsearch
from app.elastic_client import get_client
from app.config import ELASTIC_INDEX

router = APIRouter()
processing_done = False  # it be updated from main...

@router.get("/antisemitic-weapons")
def get_antisemitic_with_weapons():
    if not processing_done:
        return {"message": "Data not processed yet."}

    client: Elasticsearch = get_client()
    query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"Antisemitic": 1}},
                    {"exists": {"field": "weapons"}},
                ]
            }
        }
    }
    resp = client.search(index=ELASTIC_INDEX, body=query, size=1000)
    docs = [hit["_source"] for hit in resp["hits"]["hits"]]
    return {"results": docs}

@router.get("/multi-weapons")
def get_with_multiple_weapons():
    if not processing_done:
        return {"message": "Data not processed yet."}

    client: Elasticsearch = get_client()
    query = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "doc['weapons'].length >= 2 ? 1 : 0"
                },
            }
        }
    }
    resp = client.search(index=ELASTIC_INDEX, body=query, size=1000)
    docs = [hit["_source"] for hit in resp["hits"]["hits"] if len(hit["_source"].get("weapons", [])) >= 2]
    return {"results": docs}

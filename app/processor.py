from elasticsearch import Elasticsearch
from textblob import TextBlob
from app.config import ELASTIC_INDEX
from app.elastic_client import get_client

def detect_sentiment(text: str) -> str:
    """
    use TextBlob to detect sentiment of text.

    returns: "positive", "neutral", "negative"
    """
    analysis = TextBlob(text).sentiment.polarity
    if analysis > 0.1:
        return "positive"
    elif analysis < -0.1:
        return "negative"
    return "neutral"


def find_weapons_batch(client: Elasticsearch, weapons_list: list[str]) -> dict:
    """
    Use a single ElasticSearch query with highlight to detect all weapons.
    Returns a mapping: {doc_id: [weapons]}.
    """
    query = {
        "query": {
            "multi_match": {
                "query": " ".join(weapons_list),
                "fields": ["text"],
                "operator": "or"
            }
        },
        "highlight": {
            "fields": {
                "text": {
                    "number_of_fragments": 0
                }
            }
        },
        "size": 1000
    }

    resp = client.search(index=ELASTIC_INDEX, body=query)

    results = {}
    for hit in resp["hits"]["hits"]:
        doc_id = hit["_id"]
        highlights = " ".join(hit.get("highlight", {}).get("text", []))
        found = []
        for weapon in weapons_list:
            if weapon.lower() in highlights.lower():
                found.append(weapon)
        results[doc_id] = list(set(found))
    return results


def process_documents(csv_weapon_file: str):
    """
    - fetch all docs from ES
    - Add sentiment and weapns fields
    - remove irrelevent docs
    """
    client: Elasticsearch = get_client()


    # load weapons list
    with open(csv_weapon_file, "r") as f:
        weapons_list = [line.strip() for line in f if line.strip()]


    # Run one batch query to detect weapons in all docs
    weapons_map = find_weapons_batch(client, weapons_list)


    # fetch all docs
    query = {"query": {"match_all": {}}}
    resp = client.search(index=ELASTIC_INDEX, body=query, size=1000)

    for hit in resp["hits"]["hits"]:
        doc_id = hit["_id"]
        doc = hit["_source"]

        
        # Sentiment
        sentiment = detect_sentiment(doc["text"])
        # Weapons
        weapons = weapons_map.get(doc_id, [])

        # update doc
        client.update(
            index=ELASTIC_INDEX,
            id=doc_id,
            body={"doc": {"sentiment": sentiment, "weapons": weapons}},
        )

        # delete irrelevant
        if (
            doc.get("Antisemitic", 0) == 0
            and len(weapons) == 0
            and sentiment in ["positive", "neutral"]
        ):
            client.delete(index=ELASTIC_INDEX, id=doc_id)

    print("Processing completed.")


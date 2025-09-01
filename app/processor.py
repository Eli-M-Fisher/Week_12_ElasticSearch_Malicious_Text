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


def find_weapons(text: str, weapons_list: list[str]) -> list[str]:
    """
    we look for weapons from list inside text

    case insensitive, returns list of found weapons
    """
    found = []
    lower_text = text.lower()
    for weapon in weapons_list:
        if weapon.lower() in lower_text:
            found.append(weapon)
    return found


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


    # scroll all docs
    query = {"query": {"match_all": {}}}
    resp = client.search(index=ELASTIC_INDEX, body=query, size=1000)

    for hit in resp["hits"]["hits"]:
        doc_id = hit["_id"]
        doc = hit["_source"]

        
        # Sentiment
        sentiment = detect_sentiment(doc["text"])
        # Weapons
        weapons = find_weapons(doc["text"], weapons_list)

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


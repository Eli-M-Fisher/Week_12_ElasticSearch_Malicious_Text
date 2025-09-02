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

def find_weapons_in_text(text: str, weapons_list: list[str]) -> list[str]:
    """
    here i find weapons in text (case-insensitive)
    """
    found = []
    lower_text = text.lower()
    for weapon in weapons_list:
        if weapon.lower() in lower_text:
            found.append(weapon)
    return list(set(found))

def fetch_all_docs(client: Elasticsearch, index: str, batch_size: int = 1000):
    """
    and fetch all docs from Elasticsearch using PIT + Search After

    yields hits until exhausted.
    """
    pit = client.open_point_in_time(index=index, keep_alive="1m")["id"]
    search_after = None

    while True:
        body = {
            "size": batch_size,
            "sort": [{"_shard_doc": "asc"}],  # its required for search_after
            "pit": {"id": pit, "keep_alive": "1m"}
        }
        if search_after:
            body["search_after"] = search_after

        resp = client.search(body=body)
        hits = resp["hits"]["hits"]

        if not hits:
            break

        for hit in hits:
            yield hit

        search_after = hits[-1]["sort"]

    client.close_point_in_time(body={"id": pit})

def process_documents(csv_weapon_file: str):
    """
    - fetching all docswith PIT+Search after
    - add sentiment andweapons fields
    - Remove irrelevant doc
    """
    client: Elasticsearch = get_client()

    # load weapons list
    with open(csv_weapon_file, "r") as f:
        weapons_list = [line.strip() for line in f if line.strip()]

    processed = 0
    deleted = 0

    for hit in fetch_all_docs(client, ELASTIC_INDEX, batch_size=1000):
        doc_id = hit["_id"]
        doc = hit["_source"]

        sentiment = detect_sentiment(doc.get("text", ""))
        weapons = find_weapons_in_text(doc.get("text", ""), weapons_list)

        # update doc
        client.update(
            index=ELASTIC_INDEX,
            id=doc_id,
            body={"doc": {"sentiment": sentiment, "weapons": weapons}},
        )

        # and delete irrelevant
        if (
            doc.get("Antisemitic", 0) == 0
            and len(weapons) == 0
            and sentiment in ["positive", "neutral"]
        ):
            client.delete(index=ELASTIC_INDEX, id=doc_id)
            deleted += 1

        processed += 1

    print(f"Processing completed. Updated {processed} docs, deleted {deleted}.")
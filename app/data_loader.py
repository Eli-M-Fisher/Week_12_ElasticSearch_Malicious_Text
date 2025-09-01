import pandas as pd
from app.elastic_client import get_client, create_index_if_missing
from app.config import ELASTIC_INDEX

# load CSV data into Elasticsearch
def load_csv_to_elastic(csv_path: str):
    client = get_client()
    create_index_if_missing(client)

    df = pd.read_csv(csv_path)

    # Fix TweetID issues
    df["TweetID"] = df["TweetID"].astype(str)
    df = df.drop_duplicates(subset=["TweetID"], keep="first")

    # normalize dates to ISO format (with timezone colon)
    df["CreateDate"] = pd.to_datetime(df["CreateDate"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%S%z")

    # ensure no NaN in text
    df["text"] = df["text"].fillna("")


    # Iterate and index
    for _, row in df.iterrows():
        doc = {
            "TweetID": row["TweetID"],
            "CreateDate": row["CreateDate"],
            "Antisemitic": int(row["Antisemitic"]),
            "text": row["text"],
        }
        client.index(index=ELASTIC_INDEX, id=row["TweetID"], body=doc)

    print(f"Indexed {len(df)} documents into {ELASTIC_INDEX}")
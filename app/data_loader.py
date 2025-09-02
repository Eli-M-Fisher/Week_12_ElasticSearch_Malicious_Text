import pandas as pd
import uuid
from app.elastic_client import get_client, create_index_if_missing
from app.config import ELASTIC_INDEX


def clean_tweet_ids(df: pd.DataFrame) -> pd.DataFrame:
    """
    first i clean tweetID column:
    - convert notation safely
    - i ensure IDs are strings
    - and replace invalid/missing with UUID
    - Drop duplicates
    """
    cleaned_ids = []
    for val in df["TweetID"]:
        try:
            new_id = str(int(float(val)))
        except Exception:
            new_id = str(uuid.uuid4())
        cleaned_ids.append(new_id)

    df["TweetID"] = cleaned_ids
    return df

# load CSV data into Elasticsearch
def load_csv_to_elastic(csv_path: str):
    client = get_client()
    create_index_if_missing(client)

    df = pd.read_csv(csv_path)

    
    # clean TweetIDs
    df = clean_tweet_ids(df)

    # normalize dates to ISO8601 with timezone
    df["CreateDate"] = pd.to_datetime(
        df["CreateDate"], 
        utc=True, 
        errors="coerce"   # convert invalid to NaT
    ).dt.strftime("%Y-%m-%dT%H:%M:%S%z")

    # handle rows where parsing failed
    df["CreateDate"] = df["CreateDate"].fillna("1970-01-01T00:00:00+0000")


    # Iterate and index
    for _, row in df.iterrows():
        internal_id = str(uuid.uuid4())  # unique per row
        doc = {
            "InternalID": internal_id,
            "OriginalTweetID": row["TweetID"],  # keep original, even if duplicate
            "CreateDate": row["CreateDate"],
            "Antisemitic": int(row["Antisemitic"]),
            "text": row["text"],
        }
        client.index(index=ELASTIC_INDEX, id=internal_id, body=doc)


    print(f"Indexed {len(df)} documents into {ELASTIC_INDEX}")
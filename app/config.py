# configuration file for the application
ELASTIC_HOST = "http://localhost:9200"
ELASTIC_INDEX = "tweets_index"

# fields for index mapping
INDEX_MAPPING = {
    "mappings": {
        "properties": {
            "TweetID": {"type": "keyword"},
            "CreateDate": {"type": "date"},
            "Antisemitic": {"type": "integer"},
            "text": {"type": "text"},
            "sentiment": {"type": "keyword"},
            "weapons": {"type": "keyword"}
        }
    }
}
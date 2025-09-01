# configuration file for the application
ELASTIC_HOST = "http://elasticsearch:9200"
ELASTIC_INDEX = "tweets_index"

# shared state flag
PROCESSING_DONE = False

# fields for index mapping
INDEX_MAPPING = {
    "mappings": {
        "properties": {
            "TweetID": {"type": "keyword"},
            "CreateDate": {
                "type": "date",
                "format": "yyyy-MM-dd'T'HH:mm:ssZZ||yyyy-MM-dd'T'HH:mm:ssXXX"
            },
            "Antisemitic": {"type": "integer"},
            "text": {
                "type": "text",
                "analyzer": "simple",          
                "search_analyzer": "simple"
            },
            "sentiment": {"type": "keyword"},
            "weapons": {"type": "keyword"}
        }
    }
}

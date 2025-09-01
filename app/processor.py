from elasticsearch import Elasticsearch
from textblob import TextBlob
from app.config import ELASTIC_INDEX
from app.elastic_client import get_client

def detect_sentiment(text: str) -> str:


def find_weapons(text: str, weapons_list: list[str]) -> list[str]:


def process_documents(csv_weapon_file: str):


    # load weapons list


    # scroll all docs

        
        # Sentiment

        # Weapons

        # update doc


        # delete irrelevant
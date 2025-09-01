from fastapi import FastAPI
from app.data_loader import load_csv_to_elastic

app = FastAPI()

# i load data on startup
@app.on_event("startup")
def startup_event():
    load_csv_to_elastic("data/tweets_injected.csv")

# root endpoint
@app.get("/")
def root():
    return {"message": "ElasticSearch monolith is running!"}
from fastapi import FastAPI
from app.data_loader import load_csv_to_elastic
from app.processor import process_documents
from app import routes, config

app = FastAPI()

# i load data endpoint
@app.post("/load")
def load_data():
    load_csv_to_elastic("data/tweets_injected.csv")
    return {"message": "Data loaded into Elasticsearch"}

# endpoint to trigger processing
@app.post("/process")
def run_processing():
    process_documents("data/weapon_list.txt")
    config.PROCESSING_DONE = True  # update the shared flag
    return {"message": "Processing done."}


# root endpoint
@app.get("/")
def root():
    return {"message": "ElasticSearch monolith is running"}

app.include_router(routes.router)
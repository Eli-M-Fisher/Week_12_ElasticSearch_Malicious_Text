from fastapi import FastAPI
from app.data_loader import load_csv_to_elastic
from app.processor import process_documents
from app import routes

app = FastAPI()
processing_done = False  # the shared state to track if processing is done

# i load data on startup
@app.on_event("startup")
def startup_event():
    load_csv_to_elastic("data/tweets_injected.csv")


# endpoint to trigger processing
@app.post("/process")
def run_processing():
    global processing_done
    process_documents("data/weapon_list.txt")
    processing_done = True
    return {"message": "Processing done."}

app.include_router(routes.router)

# root endpoint
@app.get("/")
def root():
    return {"message": "ElasticSearch monolith is running!"}
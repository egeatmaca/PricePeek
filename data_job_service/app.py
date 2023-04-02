from fastapi import FastAPI
import uvicorn
import logging
from logs.log_config import config_logs
from scripts import scrape_and_analyze

app = FastAPI()

@app.get("/{marketplace}/{search_query}")
def index(marketplace, search_query):
    logging.info(f"Started scraping and analyzing {search_query} on {marketplace}...")
    scrape_and_analyze(marketplace, search_query)
    logging.info(f"Finished scraping and analyzing {search_query} on {marketplace}")
    return {"message": "success"}

if __name__ == "__main__":
    config_logs()
    uvicorn.run(app, host="0.0.0.0", port=3000)


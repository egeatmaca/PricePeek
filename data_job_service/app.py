from fastapi import FastAPI
import uvicorn
from jobs import scrape_and_analyze
from scrape.ScraperFactory import Marketplace
from logs.log_config import config_logs

app = FastAPI()

@app.get("/{marketplace}/{search_query}")
def index(marketplace, search_query):
    marketplace_enum = None
    if marketplace == "amazon":
        marketplace_enum = Marketplace.AMAZON
    elif marketplace == "ebay":
        marketplace_enum = Marketplace.EBAY
    elif marketplace == "etsy":
        marketplace_enum = Marketplace.ETSY
    else:
        return {"message": "Marketplace not found"}

    scrape_and_analyze(marketplace_enum, search_query)

    return {"message": "success"}

if __name__ == "__main__":
    config_logs()
    uvicorn.run(app, host="0.0.0.0", port=3000)


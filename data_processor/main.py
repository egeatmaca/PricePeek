from fastapi import FastAPI
import uvicorn
from controllers.AnalysisController import AnalysisController
from logs.log_config import config_logs

app = FastAPI()

@app.get("/{marketplace}/{search_query}")
def scrape_and_analyze(marketplace, search_query):
    try:
        return AnalysisController().scrape_and_analyze(marketplace, search_query)
    except Exception as e:
        return {"message": f"error: {e}"}

if __name__ == "__main__":
    config_logs()
    uvicorn.run(app, host="0.0.0.0", port=3001)


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from routers.router import router
from logs.log_config import config_logs

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)

if __name__ == "__main__":
    config_logs()
    uvicorn.run(app, host="0.0.0.0", port=3000)

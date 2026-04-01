from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="AgentBridge API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes.logs import router as logs_router
from routes.incidents import router as incidents_router
from routes.reports import router as reports_router

app.include_router(logs_router)
app.include_router(incidents_router)
app.include_router(reports_router)

@app.get("/")
def root():
    return {"status": "AgentBridge API is running"}

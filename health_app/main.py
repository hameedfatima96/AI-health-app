from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np

from signal_processor import process_ppg_signal
from llm_agent import generate_recommendation

app = FastAPI(
    title="Open-Source Health & Lifestyle API",
    description="Backend service processing biometric pulse signals and generating personalized lifestyle tips via LLM."
)

# Request schema definitions
class HealthAnalysisRequest(BaseModel):
    raw_ppg_signal: List[float]  # Sensor data list
    sampling_rate: int = 100     # Default sampling frequency
    journal_log: str             # User daily notes / stress log

@app.get("/")
def home():
    return {"status": "online", "message": "Health Backend API is running."}

@app.post("/analyze")
async def analyze_health(data: HealthAnalysisRequest):
    if not data.raw_ppg_signal or len(data.raw_ppg_signal) < 100:
        raise HTTPException(status_code=400, detail="Invalid signal input. Need at least 100 data points.")
    
    # 1. Process biometric signal locally
    vitals = process_ppg_signal(np.array(data.raw_ppg_signal), sampling_rate=data.sampling_rate)
    
    if vitals.get("status") == "error":
        raise HTTPException(status_code=500, detail=f"Signal processing error: {vitals.get('message')}")
    
    # 2. Pass biometrics + user text to LLM Agent (RAG + Groq)
    recommendation = generate_recommendation(vitals, data.journal_log)
    
    return {
        "biometrics": vitals,
        "lifestyle_recommendation": recommendation
    }
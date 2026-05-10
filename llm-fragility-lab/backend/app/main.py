from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.engines.hallucination_hunter import HallucinationHunter

app = FastAPI()

class AnalyzeRequest(BaseModel):
    response: str
    ground_truth: str

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        hunter = HallucinationHunter()
        result = hunter.analyze(request.response, request.ground_truth)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
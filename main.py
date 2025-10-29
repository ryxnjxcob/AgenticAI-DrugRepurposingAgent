from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.pharma_agent import pharma_agent
from agents.business_agent import business_agent
from agents.ai_research_agent import ai_research_agent
from utils.pdf_generator import generate_report
import uuid
import os
import time

app = FastAPI()


class QueryRequest(BaseModel):
    query: str


@app.post("/query")
async def run_query(request: QueryRequest):
    try:
        session_id = str(uuid.uuid4())
        query = request.query
        start_time = time.time()

        # Run all 3 agents (real responses via Ollama)
        pharma_data = pharma_agent(query)
        business_data = business_agent(query)
        ai_data = ai_research_agent(query)

        duration = time.time() - start_time

        response = {
            "session_id": session_id,
            "results": {
                "pharma_agent": pharma_data,
                "business_agent": business_data,
                "ai_research_agent": ai_data,
            },
        }

        # Generate PDF with metadata
        pdf_path = generate_report(response["results"], query, duration)
        response["pdf_path"] = pdf_path
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

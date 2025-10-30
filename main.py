from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.pharma_agent import pharma_agent
from agents.business_agent import business_agent
from agents.ai_research_agent import ai_research_agent
from utils.pdf_generator import generate_report
import uuid
import os
import time

app = FastAPI()

# Allow frontend access (important for browser fetch)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for local dev; restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str


# store report path temporarily (simulating user session)
LATEST_REPORT_PATH = None


@app.post("/analyze")
async def analyze_query(request: QueryRequest):
    """
    Endpoint called by frontend Run Analysis button.
    Runs all 3 agents, returns results + internally stores the generated PDF.
    """
    global LATEST_REPORT_PATH
    try:
        session_id = str(uuid.uuid4())
        query = request.query
        start_time = time.time()

        # Run all 3 agents
        pharma_data = pharma_agent(query)
        business_data = business_agent(query)
        ai_data = ai_research_agent(query)

        duration = round(time.time() - start_time, 2)

        results = {
            "Pharma Intelligence Agent": pharma_data,
            "Business Insights Agent": business_data,
            "AI Research Agent": ai_data,
        }

        # Generate PDF
        pdf_path = generate_report(results, query, duration)
        LATEST_REPORT_PATH = pdf_path  # store path for /generate_report

        return {
            "session_id": session_id,
            "duration": duration,
            "results": results,
            "pdf_ready": True,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/generate_report")
async def get_report():
    """
    Endpoint for frontend Download Report button.
    Sends back the last generated PDF.
    """
    global LATEST_REPORT_PATH
    if not LATEST_REPORT_PATH or not os.path.exists(LATEST_REPORT_PATH):
        raise HTTPException(status_code=404, detail="No report available")

    with open(LATEST_REPORT_PATH, "rb") as f:
        pdf_bytes = f.read()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=Agentic_AI_Report.pdf"},
    )


@app.get("/")
def root():
    return {"message": "Pharma Intelligence API is running"}

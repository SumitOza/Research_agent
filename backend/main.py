from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import uvicorn
from agent_workflow import execute_research_workflow

app = FastAPI(title="Research Agent API")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    api_key: str = Field(..., description="Cerebras API Key")
    research_topic: str = Field(..., description="Research topic/question")
    target_demographic: str = Field(..., description="Target demographic")
    sample_size: int = Field(..., ge=1, le=20, description="Number of interviews (1-20)")
    num_questions: int = Field(..., ge=1, le=10, description="Number of questions per interview (1-10)")

class ResearchResponse(BaseModel):
    success: bool
    message: str
    synthesis: Optional[str] = None
    interviews: Optional[List[Dict]] = None
    questions: Optional[List[str]] = None
    error: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Research Agent API is running"}

@app.post("/api/research", response_model=ResearchResponse)
async def run_research(request: ResearchRequest):
    """Execute the research workflow"""
    try:
        result = execute_research_workflow(
            api_key=request.api_key,
            research_topic=request.research_topic,
            target_demographic=request.target_demographic,
            sample_size=request.sample_size,
            num_questions=request.num_questions
        )
        
        if result["success"]:
            return ResearchResponse(
                success=True,
                message="Research completed successfully",
                synthesis=result.get("synthesis"),
                interviews=result.get("interviews"),
                questions=result.get("questions")
            )
        else:
            return ResearchResponse(
                success=False,
                message="Research workflow failed",
                error=result.get("error")
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing research: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


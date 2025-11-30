import os

from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from graph import build_graph
from state import PipelineState

# Load environment variables (e.g., ANTHROPIC_API_KEY) from .env if present
if os.path.exists(".env"):
    load_dotenv()

app = FastAPI(
    title="AI Data Pipeline Design Assistant",
    description=(
        "Describe your cloud + Spark data pipeline scenario and get an "
        "AI-generated architecture, PySpark code, IAM design, and cost/perf tips."
    ),
    version="0.1.0",
)

graph_app = build_graph()


class PipelineRequest(BaseModel):
    description: str


class PipelineResponse(BaseModel):
    final_answer: str
    architecture: str | None = None
    pyspark_code: str | None = None
    iam_design: str | None = None
    cost_tips: str | None = None
    performance_tips: str | None = None


@app.get("/")
def root():
    return {
        "message": "AI Data Pipeline Design Assistant API",
        "usage": "POST a JSON body with {'description': '...'} to /design",
    }


@app.post("/design", response_model=PipelineResponse)
def design_pipeline(req: PipelineRequest) -> PipelineResponse:
    """Run the LangGraph pipeline for a given natural-language description."""
    state: PipelineState = {"user_query": req.description}
    out_state = graph_app.invoke(state)

    return PipelineResponse(
        final_answer=out_state.get("final_answer", ""),
        architecture=out_state.get("architecture"),
        pyspark_code=out_state.get("pyspark_code"),
        iam_design=out_state.get("iam_design"),
        cost_tips=out_state.get("cost_tips"),
        performance_tips=out_state.get("performance_tips"),
    )

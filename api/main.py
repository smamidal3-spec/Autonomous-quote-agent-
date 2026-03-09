import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from agents.pipeline import MultiAgentPipeline
from agents.schema import PipelineOutput, QuoteInput

logger = logging.getLogger("quote_api")


def _parse_allowed_origins() -> list[str]:
    raw = os.getenv("ALLOWED_ORIGINS", "*")
    return [part.strip() for part in raw.split(",") if part.strip()]


app = FastAPI(title="Autonomous Quote Agents API", version="1.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=_parse_allowed_origins(),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    pipeline = MultiAgentPipeline(models_dir="models")
except Exception as exc:
    logger.exception("Failed to load pipeline: %s", exc)
    pipeline = None


@app.get("/")
def read_root() -> dict[str, str]:
    return {"status": "ok", "message": "Autonomous Quote Agents API is running."}


@app.post("/api/v1/evaluate_quote", response_model=PipelineOutput)
def evaluate_quote(quote: QuoteInput) -> PipelineOutput:
    if not pipeline:
        raise HTTPException(
            status_code=500, detail="Machine learning models not found or loaded."
        )

    try:
        logger.info("Evaluating quote for region=%s agent=%s", quote.Region, quote.Agent_Num)
        return pipeline.execute(quote)
    except Exception as exc:
        logger.exception("Pipeline execution failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))

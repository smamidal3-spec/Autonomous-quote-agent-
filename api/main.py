from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.schema import QuoteInput, PipelineOutput
from agents.pipeline import MultiAgentPipeline

app = FastAPI(title="Autonomous Quote Agents API", version="1.0")

# Add CORS Middleware so the Next.js frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (can be restricted to frontend domain later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    pipeline = MultiAgentPipeline(models_dir="models")
except Exception as e:
    print(f"Failed to load pipeline: {e}")
    pipeline = None


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Autonomous Quote Agents API is running."}


@app.post("/api/v1/evaluate_quote", response_model=PipelineOutput)
def evaluate_quote(quote: QuoteInput):
    print("\n" + "=" * 50)
    print("🚀 [RECEIVED PAYLOAD STRICT LOGGING] 🚀")
    print(quote.model_dump_json(indent=2))
    print("=" * 50 + "\n")
    if not pipeline:
        raise HTTPException(
            status_code=500, detail="Machine learning models not found or loaded."
        )
    try:
        result = pipeline.execute(quote)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

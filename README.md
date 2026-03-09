# Autonomous Quote Agent

## Project Title
Autonomous Quote Agent: Multi-Agent Insurance Decision System

## Project Overview
A production-style multi-agent pipeline that evaluates insurance quotes through risk modeling, fraud detection, conversion prediction, personalization, premium advice, and final routing.

## Motivation
Insurance quote operations often require balancing model predictions with deterministic underwriting constraints. This project demonstrates how to combine ML outputs with strict decision policies in an explainable pipeline.

## Features
- FastAPI inference API (`/api/v1/evaluate_quote`)
- 6-agent orchestration pipeline with structured outputs
- ML + heuristic hybrid risk scoring
- Fraud detection with anomaly + rule checks
- Personalization engine for plan/add-on recommendation
- Deterministic decision router with escalation policy
- Dashboard and frontend components for interaction and visualization

## Tech Stack
- Python, FastAPI, Pydantic
- scikit-learn/XGBoost model artifacts (`.pkl`)
- SHAP for explainability
- Streamlit dashboard
- Next.js frontend components

## Architecture Explanation
Pipeline flow:
1. Agent 1 - Risk profiling
2. Agent 2 - Fraud detection
3. Agent 3 - Conversion prediction
4. Agent 4 - Personalization
5. Agent 5 - Premium advisory
6. Agent 6 - Decision routing and escalation

More details: [docs/architecture.md](docs/architecture.md)

## Installation Instructions
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run API:
```bash
uvicorn api.main:app --reload --port 8000
```

Run Streamlit dashboard:
```bash
streamlit run dashboard/app_strict.py
```

## Usage Example
```bash
curl -X POST http://127.0.0.1:8000/api/v1/evaluate_quote \
  -H "Content-Type: application/json" \
  -d @examples/sample_quote_input.json
```

## Example Output
See [examples/sample_quote_output.json](examples/sample_quote_output.json).

## Testing
Run fast unit tests:
```bash
pytest tests/test_label_normalization.py tests/test_router_logic.py -q
```

## Future Improvements
- Add model registry and versioned rollout strategy
- Add confidence calibration monitoring
- Move static thresholds into configurable policy files
- Add CI workflow with API contract and smoke tests

# Architecture

## System Components
- `api/main.py`: REST entrypoint and pipeline invocation
- `agents/`: decision agents and schema definitions
- `models/`: serialized ML artifacts
- `dashboard/`: Streamlit operational UI
- `frontend/`: exploratory Next.js interface
- `tests/`: unit + scenario tests

## Request Lifecycle
1. Client submits `QuoteInput`
2. Pipeline orchestrator invokes each agent in sequence
3. Optional agents (fraud/personalization) fail safely with defaults
4. Router emits final decision and escalation status
5. API returns full `PipelineOutput`

## Reliability Strategy
- ML outputs are bounded by deterministic business rules
- Error handling is fail-safe (clear defaults + log)
- Common label normalization avoids category mismatch bugs

See [../assets/architecture.svg](../assets/architecture.svg).

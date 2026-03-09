# Contributing

## Setup
1. Create and activate a Python virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run the API locally with `uvicorn api.main:app --reload`.
4. Run selected tests before opening a PR.

## Guidelines
- Keep agent output schemas backward-compatible.
- Prefer deterministic helper modules for business rules.
- Add tests for any routing/policy logic updates.
- Keep dashboard and API payload keys aligned.

## Pull Request Checklist
- [ ] Unit tests pass
- [ ] Docs/examples updated
- [ ] No private data or secrets committed
- [ ] Large dataset files unchanged unless required

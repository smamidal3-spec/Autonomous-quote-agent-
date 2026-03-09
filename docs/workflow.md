# Workflow

## Development Workflow
1. Update one agent at a time.
2. Run targeted unit tests for that agent's rule layer.
3. Run pipeline-level smoke tests.
4. Validate API output schema compatibility.

## Inference Workflow
1. Parse and validate incoming quote JSON.
2. Compute risk, fraud, conversion, personalization, premium, and routing outputs.
3. Return a single structured response object.

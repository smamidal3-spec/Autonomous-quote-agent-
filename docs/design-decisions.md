# Design Decisions

## Deterministic Guardrails Around ML
Critical underwriting paths are protected by explicit business rules to prevent unsafe auto-approvals.

## Fail-Safe Optional Agents
Fraud and personalization agents return stable defaults on model-loading failures, allowing core decisioning to continue.

## Shared Label Normalization Layer
Repeated salary/vehicle/coverage mappings were centralized to avoid divergence and hidden category bugs.

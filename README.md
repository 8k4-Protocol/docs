# 8k4 Protocol Documentation

Canonical documentation source for 8k4.

Production docs strategy:
- This repo is the **single source of truth** for prose docs.
- Live API schema source is `https://api.8k4protocol.com/openapi.json`.
- `https://8k4protocol.com/docs/` should be a minimal shell that points here.

Auth model:
- open/public endpoints,
- x402 for paid calls,
- optional self-serve API keys (`POST /keys/generate`).

## Contents

- **[Quickstart](quickstart.md)**
- **[API Reference](api-reference.md)**
- **[x402 Payments](x402.md)**
- **[Agent Registration](agent-registration.md)**

## Key Links

- API Base: `https://api.8k4protocol.com`
- OpenAPI: `https://api.8k4protocol.com/openapi.json`
- Website: `https://8k4protocol.com`
- Website docs shell: `https://8k4protocol.com/docs/`

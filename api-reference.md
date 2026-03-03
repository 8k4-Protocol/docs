# API Reference

Base URL: `https://api.8k4protocol.com`

## Authentication & Access

- **Public/open**: e.g. `GET /health`, `GET /agents/top`
- **x402**: paid endpoints can return `402` then be paid/retried
- **API key (optional)**: `X-API-Key` from `POST /keys/generate`

### Key endpoints

- `POST /keys/generate` (wallet signature required)
- `GET /keys/info` (requires `X-API-Key`; otherwise `401`)

### Limits

- Unauthenticated IP free tier: `50/day` for `GET /agents/{id}/score` and `GET /score/explain`
- Free self-serve key: `1,000/day`
- Legacy env-configured tiers remain supported for backward compatibility

## Endpoints

### Public
- `GET /health`
- `GET /agents/top?limit=10&offset=0&chain=base|eth|bsc`

### Scoring
- `GET /agents/{agent_id}/score?chain=base|eth|bsc` — compact score payload
- `GET /score/explain?agent_id=...&chain=...` — full explainable breakdown
- `GET /score/debug?agent_id=...&chain=...` — internal key only

### Other reads
- `GET /agents/{agent_id}/validations?chain=...&limit=...&offset=...`
- `GET /wallet/{wallet}/agents`
- `GET /wallet/{wallet}/score?agent_id=...`
- `GET /identity/{global_id}`
- `GET /stats`
- `GET /metrics`

### Metadata
- `GET /metadata/{chain}/{id}.json` (canonical hosted metadata URL)
- `GET /agents/{id}/metadata.json?chain=...` (API alias)
- `POST /metadata/nonce?agent_id=...&chain=...&content_hash=0x...`
- `POST /agents/{id}/metadata`

## Status codes

- `200` success
- `401` missing/invalid key
- `402` payment required (x402)
- `422` validation error
- `429` rate limited

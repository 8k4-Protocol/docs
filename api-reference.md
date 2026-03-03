# API Reference

Base URL: `https://api.8k4protocol.com`

## Authentication & Access

- **Public/open:** `GET /health`, `GET /stats/public`, `GET /agents/top` (free listing)
- **x402:** paid endpoints can return `402 Payment Required`, then be paid/retried
- **API key (optional):** `X-API-Key` from `POST /keys/generate`

### Key management

- `POST /keys/generate` (wallet signature required)
- `GET /keys/info` (requires `X-API-Key`; otherwise `401`)

### Limits

- Unauthenticated IP free tier: `50/day` on:
  - `GET /agents/{agent_id}/score`
  - `GET /agents/{agent_id}/score/explain`
- Free self-serve key: `1,000/day`
- Legacy env-configured tiers remain supported for backward compatibility

## Endpoints

### Public

- `GET /health`
- `GET /stats/public`
- `GET /agents/top?limit=10&offset=0&chain=base|eth|bsc`

### Scoring

- `GET /agents/{agent_id}/score?chain=base|eth|bsc` — compact score payload
- `GET /agents/{agent_id}/score/explain?chain=base|eth|bsc` — explainable output
- `GET /agents/{agent_id}/score/debug?chain=base|eth|bsc` — internal key only

### Other reads

- `GET /agents/{agent_id}/validations?chain=...&limit=...`
- `GET /wallet/{wallet}/agents?chain=...`
- `GET /wallet/{wallet}/score?chain=...&agent_id=...`
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

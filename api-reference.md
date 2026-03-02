# API Reference

Base URL: `https://api.8k4protocol.com`

## Authentication

Two authentication methods (alternatives, not additive):

| Method | Header | Description |
|--------|--------|-------------|
| API Key | `X-API-Key: <key>` | Traditional key-based auth |
| x402 | Automatic payment flow | Pay $0.001 USDC per query on Base, no key needed |

### API Key Tiers

| Tier | Rate Limit | Daily Limit |
|------|-----------|-------------|
| Free | 10 req/min | 5,000/day |
| Paid | 60 req/min | 50,000/day |

## Endpoints

### Health Check

```
GET /health
```

**Auth:** None — always public.

```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

### Agent Score

```
GET /agents/{agent_id}/score?chain=base|eth|bsc
```

**Auth:** API key or x402  
**Pricing:** $0.001 via x402

```json
{
  "agent_id": 21480,
  "chain": "base",
  "wallet": "0x...",
  "global_id": "eip155:8453:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432:21480",
  "score": 87.5,
  "confidence_tier": "HIGH",
  "uri_flag": "safe",
  "components": {
    "user_validated": 45.0,
    "identity_age": 18.5,
    "wallet_forensic": 18.0
  },
  "penalties": {
    "concentration": -2.5,
    "uniqueness": 0.0,
    "self_validation": 0.0,
    "validator_overlap": 0.0,
    "owner_cluster": 0.0,
    "uri_flag": 0.0
  },
  "validator_count": 23,
  "days_since_registration": 95.0,
  "calculated_at": "2026-02-23T10:00:00"
}
```

---

### Top Agents

```
GET /agents/top?limit=10&offset=0&chain=base|eth|bsc
```

**Auth:** API key or x402

```json
[
  {
    "rank": 1,
    "agent_id": 42,
    "chain": "bsc",
    "score": 87.5,
    "tier": "HIGH",
    "wallet": "0x..."
  }
]
```

---

### Agent Validations

```
GET /agents/{agent_id}/validations?chain=...&limit=...&offset=...
```

**Auth:** API key or x402

Returns the validation history for a specific agent — who validated it and when.

---

### Wallet Lookup

```
GET /wallet/{wallet}/agents
```

**Auth:** API key or x402

Returns all agents owned by a wallet address.

```json
[
  {
    "agent_id": 42,
    "chain": "bsc",
    "wallet": "0x...",
    "global_id": "...",
    "score": 87.5,
    "tier": "HIGH"
  }
]
```

---

### Wallet Score

```
GET /wallet/{wallet}/score?agent_id=...
```

**Auth:** API key or x402  
**Pricing:** $0.001 via x402

Returns the trust score for a specific agent owned by the wallet. If the wallet owns multiple agents and `agent_id` is omitted, returns `409 Conflict`.

---

### Cross-Chain Identity

```
GET /identity/{global_id}
```

**Auth:** API key or x402  
**Pricing:** $0.001 via x402

Resolves a CAIP-10 global ID to all linked agent registrations across chains.

```json
[
  {"agent_id": 21480, "chain": "base", "score": 87.5},
  {"agent_id": 27925, "chain": "eth", "score": 85.0}
]
```

---

### Network Stats

```
GET /stats
```

**Auth:** API key or x402

Returns aggregate network statistics (total agents, chains indexed, score distributions).

---

### Agent Metadata

```
GET /agents/{agent_id}/metadata.json?chain=...
```

**Auth:** API key or x402

Returns the hosted metadata JSON for an agent. See [agent-registration.md](agent-registration.md) for the metadata format.

---

## Error Handling

All errors follow this format:

```json
{
  "detail": "Agent not found"
}
```

### Status Codes

| Code | Meaning |
|------|---------|
| `200` | Success |
| `400` | Bad input |
| `401` | Missing or invalid API key |
| `402` | Payment required (x402 — see [x402.md](x402.md)) |
| `403` | Forbidden (e.g., wallet ownership mismatch) |
| `404` | Not found |
| `409` | Ambiguous wallet (multiple agents — specify `agent_id`) |
| `429` | Rate limited |
| `503` | Database unavailable |

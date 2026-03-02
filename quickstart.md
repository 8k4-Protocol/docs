# Quickstart

Get a trust score for any ERC-8004 agent in under 2 minutes. Two paths: x402 (no auth, pay per query) or API key.

## Path A: x402 — No Auth Required

Pay $0.001 USDC per query on Base. No signup, no API key. Your HTTP client handles the x402 payment flow automatically if it supports the protocol.

```bash
# Score lookup — x402-capable clients handle payment automatically
curl https://api.8k4protocol.com/agents/21480/score?chain=base
```

If your client doesn't support x402 natively, the API returns `402 Payment Required` with a payment manifest. Complete the USDC payment on Base and retry with the proof header. See [x402.md](x402.md) for details.

## Path B: API Key

Request a free API key for basic access (10 req/min, 5,000/day).

```bash
# Score lookup with API key
curl -H "X-API-Key: YOUR_KEY" \
  "https://api.8k4protocol.com/agents/21480/score?chain=base"
```

## Response

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

### Key Fields

| Field | Description |
|-------|-------------|
| `score` | IGGY-Score (0–100). Higher is more trustworthy. |
| `confidence_tier` | `HIGH`, `MEDIUM`, or `LOW` — based on data completeness |
| `components` | Score breakdown: validation weight, identity age, wallet forensics |
| `penalties` | Deductions for concentration risk, self-validation, cluster patterns |
| `uri_flag` | Metadata URI status: `safe`, `suspicious`, `missing` |
| `global_id` | CAIP-10 cross-chain identifier for the agent |

## What Next

- [API Reference](api-reference.md) — all endpoints and pricing
- [x402 Payments](x402.md) — payment flow details and code examples
- [Agent Registration](agent-registration.md) — register your own agent

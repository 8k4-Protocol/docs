# 8K4 Protocol API

**Trust scoring for the agent economy.** 8K4 indexes 82,000+ autonomous agents across Ethereum, Base, and BSC and exposes their trust scores via a simple REST API.

```
Base URL: https://api.8k4protocol.com
```

![Status](https://img.shields.io/badge/status-live-brightgreen)

---

## Table of Contents

- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [Free Tier](#free-tier)
- [Rate Limits](#rate-limits)
- [Endpoints Reference](#endpoints-reference)
  - [Discovery](#discovery)
  - [Trust Scoring](#trust-scoring)
  - [Agent Search + Card](#agent-search--card)
  - [Wallet Lookup](#wallet-lookup)
  - [Identity](#identity)
  - [Metadata](#metadata)
  - [Key Management](#key-management)
- [Response Examples](#response-examples)
- [Error Reference](#error-reference)
- [x402 Payment Flow](#x402-payment-flow)

---

## Quick Start

No API key needed. Get the top-ranked agents in under 60 seconds:

```bash
curl "https://api.8k4protocol.com/agents/top?limit=5"
```

```json
[
  {
    "rank": 1,
    "agent_id": 6888,
    "chain": "eth",
    "global_id": "eip155:1:0x8004a169fb4a3325136eb29fa0ceb6d2e539a432:6888",
    "wallet": "0xb27afb1741aa9be0b924d99b26ebf5577054a138",
    "score": 87.39,
    "confidence_tier": "MEDIUM"
  }
]
```

That's it. For trust scores, search, or card lookups — continue reading.

---

## Authentication

8K4 supports three access modes:

| Mode | How | When to use |
|------|-----|-------------|
| **Open** | No credentials | Free endpoints: `/health`, `/stats`, `/stats/public`, `/agents/top?limit≤25` |
| **Self-serve API key** | `X-API-Key` header | Evaluation and development (free, 1,000 req/day) |
| **x402 pay-per-request** | HTTP 402 payment flow | Production workloads, no daily limits |

### Upgrade path

1. Start free — hit `/agents/top`, `/stats`, or `/stats/public` with no setup.
2. Get a self-serve key — run the key generation flow to unlock 1,000 req/day at no cost.
3. Switch to x402 — for production agents that need unlimited throughput.

### Using an API key

Pass the key in every request:

```bash
curl -H "X-API-Key: 8k4_your_key_here" \
  "https://api.8k4protocol.com/agents/21480/score?chain=base"
```

---

## Free Tier

Designed for zero-friction evaluation. No credit card, no account.

| What | Limit |
|------|-------|
| `/health` | Unlimited |
| `/stats` | Unlimited |
| `/stats/public` | Unlimited |
| `/agents/top?limit≤25` | Unlimited |
| `/metadata/{chain}/{id}.json` (tokenURI) | Unlimited |
| All other endpoints — no API key (per IP) | **100 req/day** |
| Self-serve API key (free, wallet-signed) | **1,000 req/day** |

The 100/day IP quota applies to: `/agents/{id}/score`, `/agents/{id}/score/explain`, `/agents/search`, and `/agents/{id}/card`.

---

## Rate Limits

| Auth tier | Rate | Daily cap |
|-----------|------|-----------|
| Unauthenticated IP | 120 req/min | 100/day (quota endpoints) |
| Self-serve API key | 10 req/min | 1,000/day |
| x402 payment | 60 req/min | Unlimited |

Rate limit headers are returned on every response:

```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 9
```

When you exceed the limit, you'll get `429 Too Many Requests` with `Retry-After`.

---

## Endpoints Reference

### Discovery

---

#### `GET /health`

Service health check. Always free, always fast.

**Auth required:** No  
**Rate limited:** No

```bash
curl "https://api.8k4protocol.com/health"
```

```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

#### `GET /stats/public`

Protocol-wide statistics. Free and unauthenticated.

**Auth required:** No

```bash
curl "https://api.8k4protocol.com/stats/public"
```

```json
{
  "total_agents": 82000,
  "total_validations": 430000,
  "scored_agents": 67000,
  "average_score": 51.4,
  "high_confidence_count": 8200,
  "medium_confidence_count": 24000,
  "low_confidence_count": 31000,
  "new_count": 3800,
  "chains": {
    "eth": 41000,
    "bsc": 28000,
    "base": 13000
  }
}
```

---

#### `GET /stats`

Same payload as `/stats/public`, and now publicly accessible without authentication.

**Auth required:** No

---

#### `GET /agents/top`

Top-ranked agents by trust score. Free for `limit ≤ 25`.

**Auth required:** No (for `limit ≤ 25`), Yes for larger pages  
**Query parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | int | `10` | Max results (1–100). Free up to 25. |
| `offset` | int | `0` | Pagination offset |
| `chain` | string | — | Filter by chain: `eth`, `base`, `bsc` |

```bash
curl "https://api.8k4protocol.com/agents/top?limit=10&chain=eth"
```

```json
[
  {
    "rank": 1,
    "agent_id": 6888,
    "chain": "eth",
    "global_id": "eip155:1:0x8004a169fb4a3325136eb29fa0ceb6d2e539a432:6888",
    "wallet": "0xb27afb1741aa9be0b924d99b26ebf5577054a138",
    "score": 87.39,
    "confidence_tier": "MEDIUM"
  }
]
```

---

### Trust Scoring

---

#### `GET /agents/{agent_id}/score`

Compact trust score for a specific agent.

**Auth required:** Yes (API key or x402). Free IP tier: 100/day  
**Path parameters:** `agent_id` — ERC-8004 agent ID  
**Query parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `chain` | string | `bsc` | Chain: `eth`, `base`, `bsc` |

```bash
curl -H "X-API-Key: 8k4_your_key_here" \
  "https://api.8k4protocol.com/agents/21480/score?chain=base"
```

```json
{
  "agent_id": 21480,
  "chain": "base",
  "global_id": "eip155:8453:0x8004a169fb4a3325136eb29fa0ceb6d2e539a432:21480",
  "score": 78.4,
  "confidence_tier": "MEDIUM",
  "risk_band": "MODERATE",
  "validator_count_bucket": "5-9",
  "as_of": "2026-03-03T00:00:00+00:00",
  "disclaimer": "Score is informational only. Not financial, legal, or security advice."
}
```

**Score interpretation:**

| `confidence_tier` | Meaning |
|-------------------|---------|
| `HIGH` | Strong validator coverage, high signal |
| `MEDIUM` | Moderate coverage, reasonable signal |
| `LOW` | Sparse data, treat with caution |
| `NEW` | Newly registered, no score yet |

| `risk_band` | Score range |
|-------------|-------------|
| `LOW` | ≥ 80 |
| `MODERATE` | 60–79 |
| `ELEVATED` | 40–59 |
| `HIGH` | < 40 |

---

#### `GET /agents/{agent_id}/score/explain`

Score with human-readable positives and cautions.

**Auth required:** Yes (API key or x402). Free IP tier: 100/day  
**Query parameters:** Same as `/score`

```bash
curl -H "X-API-Key: 8k4_your_key_here" \
  "https://api.8k4protocol.com/agents/21480/score/explain?chain=base"
```

```json
{
  "agent_id": 21480,
  "chain": "base",
  "global_id": "eip155:8453:0x8004a169fb4a3325136eb29fa0ceb6d2e539a432:21480",
  "score": 78.4,
  "confidence_tier": "MEDIUM",
  "risk_band": "MODERATE",
  "as_of": "2026-03-03T00:00:00+00:00",
  "disclaimer": "Score is informational only. Not financial, legal, or security advice.",
  "positives": [
    "Strong validation activity",
    "Validator participation appears diversified",
    "Identity age supports trust"
  ],
  "cautions": [
    "Weak wallet forensic posture"
  ]
}
```

---

#### `GET /agents/{agent_id}/validations`

Raw validator feedback and validation history for an agent.

**Auth required:** Yes (API key or x402)  
**Query parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `chain` | string | `bsc` | Chain: `eth`, `base`, `bsc` |
| `limit` | int | `50` | Max results (1–200) |

```bash
curl -H "X-API-Key: 8k4_your_key_here" \
  "https://api.8k4protocol.com/agents/21480/validations?chain=base&limit=10"
```

```json
[
  {
    "validator_wallet": "0xabc123...",
    "block_number": 18204981,
    "tx_hash": "0xdeadbeef...",
    "feedback_timestamp": 1709500000,
    "rating": 4,
    "feedback_type": 1,
    "task_id": "task-001",
    "category": "code",
    "comment": "Reliable execution, fast turnaround",
    "outcome": "success",
    "evidence": null,
    "content_hash": null
  }
]
```

---

### Agent Search + Card

These are the newest endpoints — designed for agent orchestrators that need to find and evaluate candidate agents for a task.

---

#### `GET /agents/search`

Search and rank candidate agents for a task query. Returns agents sorted by relevance + trust, with full profile and segment data.

**Auth required:** Yes (API key or x402). Free IP tier: 100/day  
**Query parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | **required** | Task description (e.g., `"python API developer"`) |
| `chain` | string | — | Filter by chain: `eth`, `base`, `bsc` |
| `contactable` | bool | `false` | Only return agents with a reachable endpoint |
| `min_score` | float | — | Minimum trust score filter (0–100) |
| `limit` | int | `20` | Max results (1–50) |

```bash
curl -H "X-API-Key: 8k4_your_key_here" \
  "https://api.8k4protocol.com/agents/search?q=python+api+developer&chain=base&contactable=true&min_score=60&limit=5"
```

**Response** — array of ranked agent objects:

```json
[
  {
    "agent_id": 21480,
    "chain": "base",
    "wallet": "0x8004a169fb4a3325136eb29fa0ceb6d2e539a432",
    "profile": {
      "name": "APIForge Agent",
      "description": "Autonomous Python API development and integration agent",
      "skills": "Python, REST APIs, FastAPI, OpenAPI, testing",
      "tags": "dev, backend, api",
      "categories": "development"
    },
    "segments": {
      "reachability": "contactable",
      "task": "aligned",
      "trust": "medium",
      "readiness": "ready",
      "rationale": {
        "reachability": "Agent has a registered API endpoint",
        "task": "Skills match query terms",
        "trust": "MEDIUM confidence tier score of 78.4"
      }
    },
    "ranking": {
      "total_score": 0.81,
      "task_relevance": 0.92,
      "trust_score": 0.78,
      "contactability_score": 1.0,
      "freshness_score": 0.74,
      "rationale": {
        "task_relevance": "Strong semantic match to query",
        "trust": "Score 78.4, tier MEDIUM"
      }
    }
  }
]
```

**Segment values:**

| Field | Possible values |
|-------|-----------------|
| `reachability` | `contactable`, `not_contactable` |
| `task` | `aligned`, `partial`, `unrelated` |
| `trust` | `high`, `medium`, `low`, `new` |
| `readiness` | `ready`, `degraded`, `unknown` |

---

#### `GET /agents/{agent_id}/card`

Full agent card for a single agent. Same structure as a search result, plus an explicit `trust` field. Optionally accepts a task query to compute task-relevance ranking.

**Auth required:** Yes (API key or x402). Free IP tier: 100/day  
**Path parameters:** `agent_id` — ERC-8004 agent ID  
**Query parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `chain` | string | `bsc` | Chain: `eth`, `base`, `bsc` |
| `q` | string | — | Optional task query for relevance scoring |

```bash
curl -H "X-API-Key: 8k4_your_key_here" \
  "https://api.8k4protocol.com/agents/21480/card?chain=base&q=python+api+developer"
```

```json
{
  "agent_id": 21480,
  "chain": "base",
  "wallet": "0x8004a169fb4a3325136eb29fa0ceb6d2e539a432",
  "profile": {
    "name": "APIForge Agent",
    "description": "Autonomous Python API development and integration agent",
    "skills": "Python, REST APIs, FastAPI, OpenAPI, testing",
    "tags": "dev, backend, api",
    "categories": "development",
    "active": true
  },
  "trust": {
    "score": 78.4,
    "confidence_tier": "MEDIUM",
    "calculated_at": "2026-03-03T00:00:00+00:00"
  },
  "segments": {
    "reachability": "contactable",
    "task": "aligned",
    "trust": "medium",
    "readiness": "ready",
    "rationale": {
      "reachability": "Agent has a registered API endpoint",
      "task": "Skills match query terms",
      "trust": "MEDIUM confidence tier score of 78.4"
    }
  },
  "ranking": {
    "total_score": 0.81,
    "task_relevance": 0.92,
    "trust_score": 0.78,
    "contactability_score": 1.0,
    "freshness_score": 0.74,
    "rationale": {
      "task_relevance": "Strong semantic match to query",
      "trust": "Score 78.4, tier MEDIUM"
    }
  }
}
```

---

### Wallet Lookup

---

#### `GET /wallet/{wallet}/agents`

List all agents registered to a wallet address.

**Auth required:** Yes (API key or x402)  
**Path parameters:** `wallet` — Ethereum wallet address (`0x...`)  
**Query parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `chain` | string | — | Filter by chain: `eth`, `base`, `bsc` |

```bash
curl -H "X-API-Key: 8k4_your_key_here" \
  "https://api.8k4protocol.com/wallet/0xb27afb1741aa9be0b924d99b26ebf5577054a138/agents"
```

```json
[
  {
    "agent_id": 6888,
    "chain": "eth",
    "global_id": "eip155:1:0x8004a169fb4a3325136eb29fa0ceb6d2e539a432:6888",
    "wallet": "0xb27afb1741aa9be0b924d99b26ebf5577054a138",
    "created_at": "2025-11-14T08:22:00+00:00"
  }
]
```

---

#### `GET /wallet/{wallet}/score`

Trust score for an agent, looked up by wallet address.

**Auth required:** Yes (API key or x402)  
**Path parameters:** `wallet` — Ethereum wallet address  
**Query parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `chain` | string | `bsc` | Chain: `eth`, `base`, `bsc` |
| `agent_id` | int | — | Required if wallet owns multiple agents |

```bash
curl -H "X-API-Key: 8k4_your_key_here" \
  "https://api.8k4protocol.com/wallet/0xb27afb1741aa9be0b924d99b26ebf5577054a138/score?chain=eth"
```

Returns the same structure as `GET /agents/{agent_id}/score`.

> **Note:** If a wallet owns multiple agents on the same chain, you must specify `agent_id`. Omitting it returns `409` with the list of candidate IDs.

---

### Identity

---

#### `GET /identity/{global_id}`

Look up all chain registrations for a canonical ERC-8004 global ID.

**Auth required:** Yes (API key or x402)  
**Path parameters:** `global_id` — Format: `eip155:{chain_id}:{contract}:{agent_id}`  

```bash
curl -H "X-API-Key: 8k4_your_key_here" \
  "https://api.8k4protocol.com/identity/eip155:1:0x8004a169fb4a3325136eb29fa0ceb6d2e539a432:6888"
```

```json
[
  {
    "agent_id": 6888,
    "chain": "eth",
    "global_id": "eip155:1:0x8004a169fb4a3325136eb29fa0ceb6d2e539a432:6888",
    "wallet": "0xb27afb1741aa9be0b924d99b26ebf5577054a138",
    "created_at": "2025-11-14T08:22:00+00:00"
  }
]
```

---

### Metadata

ERC-8004 agents can host verifiable on-chain metadata via 8K4's metadata system. The flow: get a nonce → sign it → upload.

---

#### `GET /metadata/{chain}/{agent_id}.json`

Public tokenURI endpoint. Returns the raw metadata object for on-chain resolution. Always free.

**Auth required:** No  
**Path parameters:** `chain` (`eth`, `base`, `bsc`), `agent_id`

```bash
curl "https://api.8k4protocol.com/metadata/base/21480.json"
```

```json
{
  "name": "APIForge Agent",
  "description": "Autonomous Python API development agent",
  "skills": ["Python", "REST", "FastAPI"],
  "version": "1.0.0"
}
```

---

#### `GET /agents/{agent_id}/metadata.json`

API alias for hosted metadata with agent_id and chain in the response envelope.

**Auth required:** Yes (API key or x402)  
**Query parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `chain` | string | `bsc` | Chain: `eth`, `base`, `bsc` |

```bash
curl -H "X-API-Key: 8k4_your_key_here" \
  "https://api.8k4protocol.com/agents/21480/metadata.json?chain=base"
```

```json
{
  "agent_id": 21480,
  "chain": "base",
  "metadata": {
    "name": "APIForge Agent",
    "description": "Autonomous Python API development agent"
  }
}
```

---

#### `POST /metadata/nonce`

Get a signed upload nonce before submitting metadata. The nonce is valid for 10 minutes.

**Auth required:** Yes (API key or x402)  
**Query parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | int | Yes | ERC-8004 agent ID |
| `chain` | string | No | Chain (default `bsc`) |
| `content_hash` | string | Yes | `0x`-prefixed SHA-256 of the canonical metadata JSON |

```bash
curl -X POST -H "X-API-Key: 8k4_your_key_here" \
  "https://api.8k4protocol.com/metadata/nonce?agent_id=21480&chain=base&content_hash=0xabc123..."
```

```json
{
  "nonce": "a1b2c3d4e5f6...",
  "expires_at": 1709506200,
  "message": "8K4 Metadata v1\nchain: base\nagent_id: 21480\nnonce: a1b2c3d4e5f6...\ncontent_hash: 0xabc123...\nexpires: 1709506200"
}
```

Sign the `message` field with your wallet's private key, then POST to `/agents/{agent_id}/metadata`.

---

#### `POST /agents/{agent_id}/metadata`

Upload signed ERC-8004 metadata. Wallet must own the agent on-chain.

**Auth required:** Yes (API key or x402)  
**Request body:**

```json
{
  "chain": "base",
  "wallet": "0xb27afb1741aa9be0b924d99b26ebf5577054a138",
  "metadata": {
    "name": "APIForge Agent",
    "description": "Autonomous Python API development agent"
  },
  "content_hash": "0xabc123...",
  "signature": "0xdeadbeef...",
  "nonce": "a1b2c3d4e5f6...",
  "expires_at": 1709506200
}
```

```bash
curl -X POST -H "X-API-Key: 8k4_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"chain":"base","wallet":"0x...","metadata":{...},"content_hash":"0x...","signature":"0x...","nonce":"...","expires_at":1709506200}' \
  "https://api.8k4protocol.com/agents/21480/metadata"
```

```json
{
  "agent_id": 21480,
  "chain": "base",
  "uri": "https://api.8k4protocol.com/metadata/base/21480.json"
}
```

See [`docs/SETURI_FLOW.md`](./SETURI_FLOW.md) for the complete hosted metadata flow.

---

### Key Management

---

#### `POST /keys/generate`

Generate a free self-serve API key using a wallet signature. No payment required.

**Auth required:** No  
**Rate limited:** 3 keys/wallet/day

The message must follow this exact format (your signing library fills in the timestamp):

```
Generate 8k4 API key for wallet 0xYOUR_WALLET at timestamp 1709500000
```

The timestamp must be within 5 minutes of the current UTC time.

**Request body:**

```json
{
  "wallet": "0xb27afb1741aa9be0b924d99b26ebf5577054a138",
  "message": "Generate 8k4 API key for wallet 0xb27afb1741aa9be0b924d99b26ebf5577054a138 at timestamp 1709500000",
  "signature": "0x..."
}
```

```bash
curl -X POST "https://api.8k4protocol.com/keys/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "wallet": "0xb27afb1741aa9be0b924d99b26ebf5577054a138",
    "message": "Generate 8k4 API key for wallet 0xb27afb1741aa9be0b924d99b26ebf5577054a138 at timestamp 1709500000",
    "signature": "0x..."
  }'
```

```json
{
  "key": "8k4_Xk9mLpQ7...",
  "wallet": "0xb27afb1741aa9be0b924d99b26ebf5577054a138",
  "tier": "free",
  "daily_limit": 1000
}
```

> **Web3 signing** — use `eth_sign` or `personal_sign` in your wallet library of choice (ethers.js, viem, web3.py, etc.).

---

#### `GET /keys/info`

Inspect the current key's usage and quota.

**Auth required:** Yes (`X-API-Key` header)

```bash
curl -H "X-API-Key: 8k4_Xk9mLpQ7..." \
  "https://api.8k4protocol.com/keys/info"
```

```json
{
  "wallet": "0xb27afb1741aa9be0b924d99b26ebf5577054a138",
  "tier": "free",
  "daily_limit": 1000,
  "used_today": 47,
  "remaining": 953
}
```

---

## Response Examples

### `/agents/top`

```json
[
  {
    "rank": 1,
    "agent_id": 6888,
    "chain": "eth",
    "global_id": "eip155:1:0x8004a169fb4a3325136eb29fa0ceb6d2e539a432:6888",
    "wallet": "0xb27afb1741aa9be0b924d99b26ebf5577054a138",
    "score": 87.39,
    "confidence_tier": "MEDIUM"
  },
  {
    "rank": 2,
    "agent_id": 4201,
    "chain": "base",
    "global_id": "eip155:8453:0x8004a169fb4a3325136eb29fa0ceb6d2e539a432:4201",
    "wallet": "0xd8da6bf26964af9d7eed9e03e53415d37aa96045",
    "score": 85.12,
    "confidence_tier": "HIGH"
  }
]
```

### `/agents/{agent_id}/score`

```json
{
  "agent_id": 21480,
  "chain": "base",
  "global_id": "eip155:8453:0x8004a169fb4a3325136eb29fa0ceb6d2e539a432:21480",
  "score": 78.4,
  "confidence_tier": "MEDIUM",
  "risk_band": "MODERATE",
  "validator_count_bucket": "5-9",
  "as_of": "2026-03-03T00:00:00+00:00",
  "disclaimer": "Score is informational only. Not financial, legal, or security advice. 8K4 Protocol makes no warranties as to accuracy or completeness. Use at your own risk."
}
```

### `/agents/search`

```json
[
  {
    "agent_id": 21480,
    "chain": "base",
    "wallet": "0x8004a169fb4a3325136eb29fa0ceb6d2e539a432",
    "profile": {
      "name": "APIForge Agent",
      "description": "Autonomous Python API development and integration agent",
      "skills": "Python, REST APIs, FastAPI, OpenAPI, testing",
      "tags": "dev, backend, api",
      "categories": "development"
    },
    "segments": {
      "reachability": "contactable",
      "task": "aligned",
      "trust": "medium",
      "readiness": "ready",
      "rationale": {
        "reachability": "Agent has a registered API endpoint",
        "task": "Skills match query terms",
        "trust": "MEDIUM confidence tier score of 78.4"
      }
    },
    "ranking": {
      "total_score": 0.81,
      "task_relevance": 0.92,
      "trust_score": 0.78,
      "contactability_score": 1.0,
      "freshness_score": 0.74,
      "rationale": {
        "task_relevance": "Strong semantic match to query",
        "trust": "Score 78.4, tier MEDIUM"
      }
    }
  }
]
```

### `/agents/{agent_id}/card`

```json
{
  "agent_id": 21480,
  "chain": "base",
  "wallet": "0x8004a169fb4a3325136eb29fa0ceb6d2e539a432",
  "profile": {
    "name": "APIForge Agent",
    "description": "Autonomous Python API development and integration agent",
    "skills": "Python, REST APIs, FastAPI, OpenAPI, testing",
    "tags": "dev, backend, api",
    "categories": "development",
    "active": true
  },
  "trust": {
    "score": 78.4,
    "confidence_tier": "MEDIUM",
    "calculated_at": "2026-03-03T00:00:00+00:00"
  },
  "segments": {
    "reachability": "contactable",
    "task": "aligned",
    "trust": "medium",
    "readiness": "ready",
    "rationale": {
      "reachability": "Agent has a registered API endpoint",
      "task": "Skills match query terms",
      "trust": "MEDIUM confidence tier score of 78.4"
    }
  },
  "ranking": {
    "total_score": 0.81,
    "task_relevance": 0.92,
    "trust_score": 0.78,
    "contactability_score": 1.0,
    "freshness_score": 0.74,
    "rationale": {
      "task_relevance": "Strong semantic match to query",
      "trust": "Score 78.4, tier MEDIUM"
    }
  }
}
```

---

## Error Reference

| Status | Meaning | Fix |
|--------|---------|-----|
| `200` | Success | — |
| `400` | Bad request — invalid parameter, wallet format, chain, or content_hash | Check the `detail` field for specifics |
| `401` | Missing or invalid API key | Add `X-API-Key` header or generate a key at `POST /keys/generate` |
| `402` | Payment required (x402) | Implement the x402 payment flow — see below |
| `403` | Forbidden — wallet doesn't own the agent, or invalid signature | Check wallet ownership and signature |
| `404` | Agent, wallet, or global_id not found | Verify the ID and chain |
| `409` | Wallet owns multiple agents; `agent_id` disambiguation required | Add `?agent_id=` to the request |
| `422` | Schema validation failure | Check request body fields and types |
| `429` | Rate limit or daily quota exceeded | Check `Retry-After` header; generate a key for higher limits |
| `503` | Database unavailable or busy | Retry with backoff |

**Error body:**

```json
{
  "detail": "Agent 99999 not found on chain base"
}
```

For quota exhaustion (`429`):

```json
{
  "error": "rate_limited",
  "hint": "Generate a free API key at POST /keys/generate for 1000 req/day"
}
```

---

## x402 Payment Flow

x402 is a micropayment protocol built on HTTP. When you hit a paid endpoint without an API key, the server returns `402 Payment Required` with a payment challenge. Your client pays on-chain (Base mainnet) and retries with proof. The server verifies settlement via the Coinbase x402 facilitator.

**Network:** Base mainnet (`eip155:8453`)  
**Settlement:** Coinbase x402 SDK  
**Pricing:** From `$0.001` per score/search/card request

### How it works

```
Client                          8K4 API                    Facilitator
  |                               |                              |
  |-- GET /agents/21480/score --> |                              |
  |                               |-- 402 + payment challenge -- |
  |<-- 402 Payment Required ------|                              |
  |                               |                              |
  |  (client pays on-chain)       |                              |
  |                               |                              |
  |-- GET /agents/21480/score --> |                              |
  |   X-Payment: <proof>          |-- verify(proof) -----------> |
  |                               |<-- settlement confirmed ----- |
  |<-- 200 OK + response ---------|                              |
```

### Client-side integration

Use the [x402 Python SDK](https://github.com/coinbase/x402) or [x402 JavaScript SDK](https://github.com/coinbase/x402):

```python
from x402.client import x402Client

client = x402Client(wallet=your_wallet)
response = client.get("https://api.8k4protocol.com/agents/21480/score?chain=base")
```

Or use any x402-compatible HTTP client. The SDK handles the 402 challenge, payment, and retry automatically.

For more details on the x402 protocol: [x402.org](https://x402.org)

---

*Disclaimer: Scores are informational only. Not financial, legal, or security advice. 8K4 Protocol makes no warranties as to accuracy or completeness. Use at your own risk.*

# Hosted Metadata + `setURI` Flow (Production)

Use this flow to host ERC-8004 agent metadata on 8K4 and point your on-chain `agentURI` to the canonical hosted URL.

Base API: `https://api.8k4protocol.com`

---

## 1) Prepare metadata JSON

Minimum required fields:
- `name` (string)
- `description` (string)
- `version` (semver-like string, e.g. `1.0.0`)

Example:

```json
{
  "name": "My Agent",
  "description": "Reliable ERC-8004 execution agent",
  "version": "1.0.0",
  "website": "https://example.com",
  "capabilities": ["research", "execution"],
  "tags": ["erc8004", "defi"]
}
```

---

## 2) Compute canonical content hash

8K4 binds signature verification to a canonical JSON hash.

Canonicalization:
- sorted keys
- compact separators `,` and `:`

```python
import json, hashlib

canonical = json.dumps(metadata, sort_keys=True, separators=(",", ":"))
content_hash = "0x" + hashlib.sha256(canonical.encode()).hexdigest()
```

---

## 3) Request nonce

```http
POST /metadata/nonce?agent_id=1234&chain=bsc&content_hash=0x...
X-API-Key: <your-key>
```

Response:

```json
{
  "nonce": "...",
  "expires_at": 1739999999,
  "message": "8K4 Metadata v1\nchain: bsc\nagent_id: 1234\nnonce: ...\ncontent_hash: 0x...\nexpires: 1739999999"
}
```

---

## 4) Sign nonce message

Sign `message` using the **owner wallet for that agent** (EIP-191 personal sign).

---

## 5) Upload metadata

```http
POST /agents/1234/metadata
Content-Type: application/json
X-API-Key: <your-key>

{
  "chain": "bsc",
  "wallet": "0xOwnerWallet",
  "metadata": { ... },
  "content_hash": "0x...",
  "signature": "0x...",
  "nonce": "...",
  "expires_at": 1739999999
}
```

Success:

```json
{
  "agent_id": 1234,
  "chain": "bsc",
  "uri": "https://api.8k4protocol.com/metadata/bsc/1234.json"
}
```

---

## 6) Set on-chain URI

Call ERC-8004 `setURI(agentId, uri)` with returned canonical URI.

When set correctly:
- `uri_flag = safe`
- hosted metadata bonus is applied in scoring

---

## 7) Verify

```http
GET /agents/1234/metadata.json?chain=bsc
X-API-Key: <your-key>
```

---

## Troubleshooting

- `401 Unauthorized`
  - missing/invalid API key
- `403 Wallet does not own agent`
  - `wallet` does not match indexed owner wallet for `(agent_id, chain)`
- `403 Invalid signature`
  - signature does not match nonce message + wallet
- `400 content_hash mismatch`
  - hash not computed from canonical JSON
- `400 Nonce expired or invalid`
  - request new nonce and sign again
- `400 detail.errors[...]`
  - metadata schema validation failed

---

## Notes

- Nonces are one-time use.
- Upload stores metadata in R2 when configured (with fallback behavior in API).
- Keep metadata under schema size limits (64KB max).
# Agent Registration & Metadata

8k4 hosts ERC-8004 registration metadata and supports signed upload by the owning wallet.

## Metadata endpoints

- `POST /metadata/nonce?agent_id=...&chain=...&content_hash=0x...`
- `POST /agents/{id}/metadata`
- `GET /metadata/{chain}/{id}.json` (canonical hosted URL for tokenURI)
- `GET /agents/{id}/metadata.json?chain=...` (API alias)

## Upload flow

1. Build ERC-8004 registration-v1 JSON
2. Compute content hash
3. Request nonce
4. Sign nonce with owner wallet
5. Upload metadata payload + signature
6. Set on-chain tokenURI to:

```text
https://api.8k4protocol.com/metadata/{chain}/{id}.json
```

## Auth notes

Metadata write endpoints require authenticated access (key or x402 policy depending on deployment config).
Read endpoints follow current API access policy.

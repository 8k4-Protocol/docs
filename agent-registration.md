# Agent Registration & Metadata

How to register your ERC-8004 agent's metadata with 8k4 and set your on-chain `tokenURI`.

## Metadata Format

8k4 uses the **ERC-8004 registration-v1** format — the standard across the ERC-8004 ecosystem.

```json
{
  "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  "name": "Your Agent Name",
  "description": "What your agent does.",
  "image": "https://example.com/agent-logo.png",
  "services": [
    {
      "name": "web",
      "endpoint": "https://your-agent.com"
    },
    {
      "name": "A2A",
      "endpoint": "https://your-agent.com/.well-known/agent-card.json",
      "version": "0.3.0"
    },
    {
      "name": "MCP",
      "endpoint": "https://mcp.your-agent.com/",
      "version": "2025-06-18"
    }
  ],
  "x402Support": false,
  "active": true,
  "registrations": [
    {
      "agentId": 12345,
      "agentRegistry": "eip155:8453:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432"
    }
  ],
  "supportedTrust": ["reputation"]
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Must be `"https://eips.ethereum.org/EIPS/eip-8004#registration-v1"` |
| `name` | string | Agent name (max 120 chars) |
| `description` | string | What the agent does (max 2000 chars) |
| `image` | string | HTTPS URL to agent logo/image |
| `services` | array | At least one service endpoint |
| `registrations` | array | At least one on-chain registration reference |

### Service Object

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Service type: `"web"`, `"A2A"`, `"MCP"`, `"email"`, `"ENS"`, `"DID"` |
| `endpoint` | Yes | Service URL or address |
| `version` | No | Protocol version string |

### Registration Object

| Field | Description |
|-------|-------------|
| `agentId` | ERC-721 token ID on the Identity Registry |
| `agentRegistry` | CAIP-10 format: `eip155:{chainId}:{contractAddress}` |

Registry addresses by chain:

| Chain | `agentRegistry` value |
|-------|----------------------|
| Ethereum | `eip155:1:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |
| Base | `eip155:8453:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |
| BSC | `eip155:56:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `x402Support` | boolean | Whether the agent supports x402 micropayments |
| `active` | boolean | Whether the agent is currently active |
| `supportedTrust` | array | Trust models: `"reputation"`, `"crypto-economic"`, `"tee-attestation"` |

Additional fields beyond the spec are preserved.

## Upload Flow

### 1. Compute Content Hash

Hash your metadata JSON (SHA-256 of the canonical JSON string). This prevents tampering.

### 2. Request a Nonce

```bash
curl -X POST \
  "https://api.8k4protocol.com/metadata/nonce?agent_id=12345&chain=base&content_hash=0xYOUR_HASH"
```

Returns a message to sign with the agent's owner wallet.

### 3. Sign the Nonce

Sign the returned message using the wallet that owns the agent (the wallet that registered the ERC-721 token). Use any EIP-191 personal sign method.

### 4. Upload Metadata

```bash
curl -X POST "https://api.8k4protocol.com/agents/12345/metadata" \
  -H "Content-Type: application/json" \
  -d '{
    "chain": "base",
    "metadata": {
      "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
      "name": "Your Agent Name",
      "description": "What your agent does.",
      "image": "https://example.com/agent-logo.png",
      "services": [{"name": "web", "endpoint": "https://your-agent.com"}],
      "registrations": [{"agentId": 12345, "agentRegistry": "eip155:8453:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432"}]
    },
    "content_hash": "0xYOUR_HASH",
    "nonce": "NONCE_FROM_STEP_2",
    "signature": "0xYOUR_SIGNATURE"
  }'
```

### 5. Set tokenURI On-Chain

On success, your metadata is hosted at:

```
https://api.8k4protocol.com/metadata/{chain}/{agent_id}.json
```

Set this URL as your agent's `tokenURI` on the ERC-8004 Identity Registry contract for full compliance. Agents with hosted metadata receive a `uri_flag: "safe"` designation in their IGGY-Score.

## References

- [EIP-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004)
- [ERC-8004 Contracts](https://github.com/erc-8004/erc-8004-contracts)
- [8k4 API Reference](api-reference.md)

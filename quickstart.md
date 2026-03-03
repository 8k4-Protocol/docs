# Quickstart

Two ways to access 8k4 paid scoring endpoints:

1. **x402** (no key, pay per request)
2. **Optional API key** (self-serve via wallet signature)

## 1) Public sanity check

```bash
curl "https://api.8k4protocol.com/agents/top?limit=5"
# -> 200 OK
```

## 2) x402 flow (paid endpoint)

```bash
curl "https://api.8k4protocol.com/agents/21480/score?chain=base"
# -> 402 Payment Required (without key/payment proof)
```

Use an x402-capable client to pay on Base and retry automatically.

## 3) Optional self-serve key flow

```bash
curl -X POST "https://api.8k4protocol.com/keys/generate" \
  -H "Content-Type: application/json" \
  -d '{"wallet":"0xYOUR_WALLET","message":"8k4 key request","signature":"0x..."}'
```

Then call paid endpoints with `X-API-Key`:

```bash
curl -H "X-API-Key: YOUR_KEY" \
  "https://api.8k4protocol.com/agents/21480/score?chain=base"
```

Check key status/usage:

```bash
curl -H "X-API-Key: YOUR_KEY" "https://api.8k4protocol.com/keys/info"
```

Without key, `/keys/info` returns `401`.

## Limits

- Unauthenticated IP free tier: `50/day` for score + explain endpoints
- Free self-serve API key: `1,000/day`

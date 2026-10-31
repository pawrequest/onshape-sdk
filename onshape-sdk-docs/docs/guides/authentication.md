---
sidebar_position: 2
title: Authentication
---

# Authentication

The SDK uses **HMAC-SHA256 API key authentication** as specified by the [Onshape API documentation](https://onshape-public.github.io/docs/api-intro/explorer/#authentication).

## How It Works

Every API request is signed with your secret key. The SDK handles this automatically, but here's what happens under the hood:

### 1. Signing String Construction

A canonical string is built from the request details:

```
method + "\n" + nonce + "\n" + date + "\n" + content_type + "\n" + path + "\n" + query + "\n"
```

The **entire string is lowercased** before signing.

### 2. HMAC-SHA256 Signature

The signing string is hashed using your secret key:

```python
signature = base64(hmac_sha256(secret_key, signing_string))
```

### 3. Request Headers

Four headers are sent with every request:

| Header | Value |
|--------|-------|
| `Authorization` | `On {access_key}:HmacSHA256:{signature}` |
| `Date` | RFC 2616 date (e.g., `Tue, 18 Mar 2026 00:00:00 GMT`) |
| `On-Nonce` | Random 25-character alphanumeric string |
| `Content-Type` | `application/json` |

:::warning Common Pitfall
The nonce goes **only** in the `On-Nonce` header — **not** in the `Authorization` header. This is the most common authentication bug.
:::

## Creating a Client

### From Environment Variables

The simplest approach — reads `ONSHAPE_ACCESS_KEY` and `ONSHAPE_SECRET_KEY` from a `.env` file:

```python
from onshape_sdk import OnshapeClient

client = OnshapeClient.from_env()
```

### Direct Initialization

```python
client = OnshapeClient(
    access_key="your_access_key",
    secret_key="your_secret_key",
)
```

### Custom Base URL

For Onshape Enterprise instances:

```python
client = OnshapeClient.from_env(
    base_url="https://your-company.onshape.com"
)
```

## Testing Authentication

```python
result = client.test_auth()
```

This calls two endpoints to verify your credentials:

1. `GET /api/v6/users/sessioninfo` — confirms your API keys are valid
2. `GET /api/v6/documents` — confirms you can access documents

### Example Output

```json
{
  "user": "Zach Sharma (zach@example.com)",
  "documents_accessible": 42
}
```

### Common Errors

| Status | Meaning |
|--------|---------|
| `401` | Invalid access key or secret key |
| `403` | Key is valid but lacks permission for the resource |
| `404` | Document or element doesn't exist |

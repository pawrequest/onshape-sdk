---
sidebar_position: 4
title: Error Handling
---

# Error Handling

## HTTP Errors

All API methods raise `requests.HTTPError` on non-2xx responses. The SDK automatically includes the response body in the error message:

```python
try:
    doc = client.documents.get("nonexistent_id")
except Exception as e:
    print(e)
    # 404 Client Error: Not Found — {"message": "Document not found"}
```

### Common Status Codes

| Code | Meaning | Typical Cause |
|------|---------|---------------|
| `400` | Bad Request | Invalid parameters or malformed body |
| `401` | Unauthorized | Invalid API keys |
| `403` | Forbidden | Valid keys but no access to this resource |
| `404` | Not Found | Document/element/part doesn't exist |
| `409` | Conflict | Concurrent edit conflict |
| `429` | Too Many Requests | Rate limit exceeded |

## Translation Errors

The `TranslationsApi` raises `TranslationError` for failed or timed-out export jobs:

```python
from onshape_sdk.translations import TranslationError

try:
    client.translations.export(
        did=did, wvm="w", wvm_id=wid, eid=eid,
        format_name="DXF",
        output_path="output.dxf",
        timeout=60,
    )
except TranslationError as e:
    print(f"Export failed: {e}")
```

### TranslationError Scenarios

- **Job failure** — Onshape returned `requestState: "FAILED"` with a `failureReason`
- **Timeout** — the job didn't complete within the specified timeout (default 300 seconds)

## URL Parse Errors

`parse_onshape_url` raises `ValueError` for invalid URLs:

```python
from onshape_sdk import parse_onshape_url

try:
    ids = parse_onshape_url("https://google.com")
except ValueError as e:
    print(e)  # "Could not parse Onshape URL: https://google.com"
```

## Retry Strategy

The SDK doesn't include built-in retries. For production use, wrap calls with a retry library:

```python
import time

def retry(fn, retries=3, delay=2):
    for i in range(retries):
        try:
            return fn()
        except Exception as e:
            if i == retries - 1:
                raise
            time.sleep(delay * (i + 1))

parts = retry(lambda: client.parts.list(did, "w", wid, eid))
```

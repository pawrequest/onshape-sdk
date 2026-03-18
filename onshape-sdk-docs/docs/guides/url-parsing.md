---
sidebar_position: 3
title: URL Parsing
---

# URL Parsing

Onshape document URLs contain all the IDs needed to make API calls. The SDK provides helpers to extract them.

## URL Format

```
https://cad.onshape.com/documents/{did}/{w|v|m}/{wvm_id}/e/{eid}
```

| Component | Description |
|-----------|-------------|
| `did` | Document ID |
| `w` / `v` / `m` | Workspace, Version, or Microversion selector |
| `wvm_id` | ID of the workspace, version, or microversion |
| `eid` | Element ID (Part Studio, Assembly, Drawing, etc.) |

## parse_onshape_url

Extracts all four IDs from a full Onshape URL:

```python
from onshape_sdk import parse_onshape_url

url = "https://cad.onshape.com/documents/804d1a7a071db077dbad4e42/w/c9f128ed004c27e492b8cebb/e/58863216bdaab008805f5f3f"
ids = parse_onshape_url(url)
```

### Return Value

Returns an `OnshapeIds` TypedDict:

```python
{
    "did": "804d1a7a071db077dbad4e42",
    "wvm_type": "w",
    "wvm_id": "c9f128ed004c27e492b8cebb",
    "eid": "58863216bdaab008805f5f3f"
}
```

### Using with API Calls

The parsed IDs can be spread directly into any API method:

```python
ids = parse_onshape_url(url)

# List parts
parts = client.parts.list(
    ids["did"], ids["wvm_type"], ids["wvm_id"], ids["eid"]
)

# Export DXF
client.translations.export(
    did=ids["did"],
    wvm=ids["wvm_type"],
    wvm_id=ids["wvm_id"],
    eid=ids["eid"],
    format_name="DXF",
    output_path="output.dxf",
)
```

## build_wvm_path

Builds the common `/d/{did}/{wvm}/{wvm_id}/e/{eid}` path fragment used in most API routes:

```python
from onshape_sdk import build_wvm_path

# With element ID
path = build_wvm_path("abc123", "w", "def456", eid="789fed")
# → "/d/abc123/w/def456/e/789fed"

# Without element ID
path = build_wvm_path("abc123", "v", "def456")
# → "/d/abc123/v/def456"
```

This is used internally by all resource API modules but is available for custom API calls.

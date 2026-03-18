---
sidebar_position: 6
title: TranslationsApi
---

# TranslationsApi

Async CAD format translation (export/import). Supports STEP, IGES, STL, DXF, DWG, PDF, SOLIDWORKS, RHINO, OBJ, GLTF, CATIA, JT, and 3MF.

```python
trans_api = client.translations
```

**Base path:** `/api/v6/.../translations`

## Supported Formats

```python
TranslationsApi.FORMATS = [
    "STEP", "IGES", "STL", "DXF", "DWG", "PDF",
    "SOLIDWORKS", "RHINO", "OBJ", "GLTF", "CATIA", "JT", "3MF"
]
```

## High-Level Export

### export

The recommended way to export — handles the full create → poll → download → save pipeline automatically.

```python
translations.export(
    did: str, wvm: str, wvm_id: str, eid: str,
    format_name: str,
    output_path: str,
    element_type: str = "PARTSTUDIO",
    part_ids: list[str] | None = None,
    timeout: int = 300,
    poll_interval: int = 2,
    verbose: bool = False,
    **extra_body
) -> str  # returns output_path
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `format_name` | `str` | *required* | One of `FORMATS` (e.g., `"STEP"`, `"DXF"`) |
| `output_path` | `str` | *required* | Local file path to save to |
| `element_type` | `str` | `"PARTSTUDIO"` | `"PARTSTUDIO"` or `"ASSEMBLY"` |
| `part_ids` | `list[str]` | `None` | Export specific parts only |
| `timeout` | `int` | `300` | Max seconds to wait |
| `poll_interval` | `int` | `2` | Seconds between status checks |
| `verbose` | `bool` | `False` | Print progress to stdout |

```python
# Export a Part Studio as STEP
path = client.translations.export(
    did=did, wvm="w", wvm_id=wid, eid=eid,
    format_name="STEP",
    output_path="bracket.step",
    verbose=True,
)
print(f"Saved to {path}")
```

**Console output (verbose=True):**

```
[Translation] Created job abc123-def456
[Translation] Polling... ACTIVE
[Translation] Polling... ACTIVE
[Translation] Polling... DONE
[Translation] Downloading...
[Translation] Saved to bracket.step (234567 bytes)
```

:::tip DXF Export
For DXF, you can also use the direct [`part_studios.export_dxf()`](./part-studios#export_dxf) method which is synchronous and simpler. The Translation API version supports more options.
:::

---

## Low-Level Methods

### create

Create a translation job.

```python
translations.create(
    did: str, wvm: str, wvm_id: str, eid: str,
    format_name: str,
    element_type: str = "PARTSTUDIO",
    part_ids: list[str] | None = None,
    store_in_document: bool = False,
    link_document_id: str | None = None,
    configuration: str | None = None,
    **extra_body
) -> TranslationStatus
```

```python
status = client.translations.create(
    did, "w", wid, eid, "STEP"
)
print(f"Job ID: {status.id}, State: {status.request_state}")
```

**Example response object:**

```json
{
  "id": "abc123-def456",
  "request_state": "ACTIVE",
  "result_external_data_ids": [],
  "failure_reason": null,
  "name": "bracket.step"
}
```

---

### get_status

Check the current state of a translation job.

```python
translations.get_status(translation_id: str) -> TranslationStatus
```

```python
status = client.translations.get_status("abc123-def456")
print(status.request_state)  # "ACTIVE", "DONE", or "FAILED"
print(status.is_done)         # True/False
print(status.is_failed)       # True/False
```

---

### wait

Block until a translation job completes or times out.

```python
translations.wait(
    translation_id: str,
    timeout: int = 300,
    poll_interval: int = 2,
    verbose: bool = False
) -> TranslationStatus
```

Raises `TranslationError` on failure or timeout.

```python
status = client.translations.wait("abc123-def456", verbose=True)
ext_id = status.result_external_data_ids[0]
```

---

### download

Download the binary result of a completed translation.

```python
translations.download(did: str, external_data_id: str) -> bytes
```

Handles the S3 redirect that Onshape returns (302 → follow → binary content).

```python
data = client.translations.download(did, ext_id)
with open("output.step", "wb") as f:
    f.write(data)
```

## Error Handling

```python
from onshape_sdk.translations import TranslationError

try:
    client.translations.export(
        did=did, wvm="w", wvm_id=wid, eid=eid,
        format_name="DXF", output_path="out.dxf",
        timeout=30,
    )
except TranslationError as e:
    print(f"Translation failed: {e}")
    # "Translation failed: ..." or "Translation timed out after 30s"
```

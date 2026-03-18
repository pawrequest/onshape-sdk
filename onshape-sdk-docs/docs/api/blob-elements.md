---
sidebar_position: 8
title: BlobElementsApi
---

# BlobElementsApi

Upload and download binary file elements (blobs) in Onshape documents.

```python
blob_api = client.blob_elements
```

**Base path:** `/api/v6/blobelements`

## Methods

### download

Download the contents of a blob element.

```python
blob_elements.download(did: str, wvm: str, wvm_id: str, eid: str) -> bytes
```

Handles the S3 redirect that Onshape uses for binary content.

```python
data = client.blob_elements.download(did, "w", wid, eid)
with open("downloaded_file.pdf", "wb") as f:
    f.write(data)
print(f"Downloaded {len(data)} bytes")
```

---

### upload

Upload a local file as a new blob element in a document.

```python
blob_elements.upload(
    did: str, wid: str,
    file_path: str,
    content_type: str | None = None
) -> dict
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `did` | `str` | *required* | Document ID |
| `wid` | `str` | *required* | Workspace ID |
| `file_path` | `str` | *required* | Path to local file |
| `content_type` | `str` | `None` | MIME type (auto-detected from extension if omitted) |

```python
result = client.blob_elements.upload(
    did, wid,
    file_path="reference.pdf",
    content_type="application/pdf",
)
print(f"Created element: {result}")
```

:::note Workspace Only
Upload only works on workspaces (`w`), not versions or microversions.
:::

---
sidebar_position: 10
title: ThumbnailsApi
---

# ThumbnailsApi

Get thumbnail preview images for documents and elements.

```python
thumb_api = client.thumbnails
```

**Base path:** `/api/v6/thumbnails`

## Methods

### get_info

Get available thumbnail sizes for a document or element.

```python
thumbnails.get_info(
    did: str, wvm: str, wvm_id: str,
    eid: str | None = None
) -> ThumbnailInfo
```

```python
info = client.thumbnails.get_info(did, "w", wid)
for size in info.sizes:
    print(f"{size.size} — {size.href}")
```

**Example response object:**

```json
{
  "sizes": [
    {"size": "70x40", "href": "https://..."},
    {"size": "300x170", "href": "https://..."},
    {"size": "600x340", "href": "https://..."}
  ]
}
```

---

### download

Download a thumbnail image as PNG bytes.

```python
thumbnails.download(
    did: str, wvm: str, wvm_id: str,
    size: str = "300x170",
    eid: str | None = None
) -> bytes
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `size` | `str` | `"300x170"` | Thumbnail dimensions (e.g., `"70x40"`, `"300x170"`, `"600x340"`) |
| `eid` | `str` | `None` | Element ID (omit for document-level thumbnail) |

```python
# Document thumbnail
png_data = client.thumbnails.download(did, "w", wid)
with open("thumb.png", "wb") as f:
    f.write(png_data)

# Element thumbnail (larger size)
png_data = client.thumbnails.download(did, "w", wid, size="600x340", eid=eid)
```

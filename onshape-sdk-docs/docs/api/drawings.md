---
sidebar_position: 7
title: DrawingsApi
---

# DrawingsApi

Access drawing element metadata, views, and view geometry.

```python
drw_api = client.drawings
```

**Base path:** `/api/v6/drawings`

## Methods

### get

Get drawing element metadata.

```python
drawings.get(did: str, wvm: str, wvm_id: str, eid: str) -> dict
```

```python
drawing = client.drawings.get(did, "w", wid, eid)
print(drawing)
```

---

### get_views

List all views in a drawing.

```python
drawings.get_views(did: str, wvm: str, wvm_id: str, eid: str) -> list[DrawingView]
```

```python
views = client.drawings.get_views(did, "w", wid, eid)
for v in views:
    print(f"{v.name} — {v.view_type}, scale={v.scale}")
```

**Example response object:**

```json
{
  "id": "view-001",
  "name": "Front View",
  "view_type": "SECTION",
  "scale": 1.0,
  "raw": { ... }
}
```

---

### get_view_geometry

Get the JSON geometry data for a specific drawing view.

```python
drawings.get_view_geometry(
    did: str, wvm: str, wvm_id: str, eid: str,
    view_id: str
) -> dict
```

```python
geom = client.drawings.get_view_geometry(did, "w", wid, eid, "view-001")
# Returns raw geometry JSON with curves, lines, arcs, etc.
```

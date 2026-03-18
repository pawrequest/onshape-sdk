---
sidebar_position: 3
title: PartsApi
---

# PartsApi

Query parts in a Part Studio — list, inspect, get mass properties and bounding boxes.

```python
parts_api = client.parts
```

**Base path:** `/api/v6/parts`

## Methods

### list

List all parts in a Part Studio element.

```python
parts.list(did: str, wvm: str, wvm_id: str, eid: str) -> list[Part]
```

```python
parts = client.parts.list(did, "w", wid, eid)
for p in parts:
    print(f"{p.name} — {p.part_id} ({p.body_type})")
```

**Example response object:**

```json
{
  "name": "Bracket",
  "part_id": "JHD",
  "body_type": "solid",
  "material": {"name": "Steel", "id": "..."},
  "appearance": {"color": {"red": 180, "green": 180, "blue": 180}},
  "raw": { ... }
}
```

---

### get

Get a single part by ID.

```python
parts.get(did: str, wvm: str, wvm_id: str, eid: str, part_id: str) -> Part
```

```python
part = client.parts.get(did, "w", wid, eid, "JHD")
print(part.name, part.material)
```

---

### get_mass_properties

Get mass, volume, centroid, and inertia tensor for parts.

```python
parts.get_mass_properties(
    did: str, wvm: str, wvm_id: str, eid: str,
    part_id: str | None = None
) -> dict
```

If `part_id` is `None`, returns mass properties for all parts in the Part Studio.

```python
props = client.parts.get_mass_properties(did, "w", wid, eid, "JHD")
print(props)
```

**Example response:**

```json
{
  "bodies": {
    "JHD": {
      "mass": [0.0234],
      "volume": [2.98e-06],
      "centroid": [0.0, 0.025, 0.0],
      "inertia": [1.2e-07, 0, 0, 0, 3.4e-07, 0, 0, 0, 2.1e-07]
    }
  }
}
```

---

### get_body_details

Get topological body details (faces, edges, vertices) for parts.

```python
parts.get_body_details(
    did: str, wvm: str, wvm_id: str, eid: str,
    part_id: str | None = None
) -> dict
```

```python
details = client.parts.get_body_details(did, "w", wid, eid)
```

---

### get_bounding_boxes

Get axis-aligned bounding boxes for parts.

```python
parts.get_bounding_boxes(
    did: str, wvm: str, wvm_id: str, eid: str,
    part_id: str | None = None
) -> dict
```

```python
bbox = client.parts.get_bounding_boxes(did, "w", wid, eid, "JHD")
print(bbox)
```

**Example response:**

```json
{
  "lowX": -0.05,
  "lowY": -0.01,
  "lowZ": -0.05,
  "highX": 0.05,
  "highY": 0.06,
  "highZ": 0.05
}
```

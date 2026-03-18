---
sidebar_position: 9
title: MetadataApi
---

# MetadataApi

Read and update custom metadata properties on elements and parts.

```python
meta_api = client.metadata
```

**Base path:** `/api/v6/metadata`

## Methods

### get

Get metadata properties for an element or a specific part.

```python
metadata.get(
    did: str, wvm: str, wvm_id: str, eid: str,
    part_id: str | None = None
) -> list[MetadataProperty]
```

```python
# Element-level metadata
props = client.metadata.get(did, "w", wid, eid)
for p in props:
    print(f"{p.name} = {p.value} ({p.value_type})")

# Part-level metadata
props = client.metadata.get(did, "w", wid, eid, part_id="JHD")
```

**Example response object:**

```json
{
  "name": "Part Number",
  "property_id": "57f3fb8efa3416c06701d61d",
  "value": "BRK-001",
  "value_type": "STRING",
  "raw": { ... }
}
```

---

### update

Update metadata properties on an element or part.

```python
metadata.update(
    did: str, wvm: str, wvm_id: str, eid: str,
    properties: list[dict],
    part_id: str | None = None
) -> dict
```

Each property dict needs `propertyId` and `value`:

```python
client.metadata.update(did, "w", wid, eid, [
    {
        "propertyId": "57f3fb8efa3416c06701d61d",
        "value": "BRK-002"
    },
    {
        "propertyId": "57f3fb8efa3416c06701d620",
        "value": "Updated bracket"
    }
])
```

:::tip Finding Property IDs
Use `metadata.get()` first to discover the `property_id` values for each metadata field. These IDs are stable and won't change.
:::

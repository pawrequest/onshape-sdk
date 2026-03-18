---
sidebar_position: 5
title: AssembliesApi
---

# AssembliesApi

Work with assemblies — get structure, BOM, mates, insert parts, and apply transforms.

```python
asm_api = client.assemblies
```

**Base path:** `/api/v6/assemblies`

## Methods

### get_definition

Get the full assembly structure including root parts and sub-assemblies.

```python
assemblies.get_definition(
    did: str, wvm: str, wvm_id: str, eid: str,
    include_mate_features: bool = True,
    include_non_solids: bool = False
) -> AssemblyDefinition
```

```python
defn = client.assemblies.get_definition(did, "w", wid, eid)
print(f"Root parts: {len(defn.root_parts)}")
print(f"Sub-assemblies: {len(defn.sub_assemblies)}")
for part in defn.parts:
    print(f"  {part.get('name', 'unnamed')}")
```

**Example response object:**

```json
{
  "root_parts": ["MR0..."],
  "parts": [
    {"partId": "JHD", "name": "Bracket", "documentId": "804d..."}
  ],
  "sub_assemblies": [],
  "raw": { ... }
}
```

---

### get_bom

Get the Bill of Materials.

```python
assemblies.get_bom(
    did: str, wvm: str, wvm_id: str, eid: str,
    indented: bool = True,
    multi_level: bool = False
) -> BomTable
```

```python
bom = client.assemblies.get_bom(did, "w", wid, eid)
print(f"Columns: {bom.headers}")
for row in bom.rows:
    print(f"  {row.item_name} × {row.quantity}")
```

**Example response object:**

```json
{
  "headers": ["Item", "Quantity", "Part Number", "Description"],
  "rows": [
    {
      "item_name": "Bracket",
      "quantity": 4,
      "item_source": 0,
      "raw": { ... }
    }
  ]
}
```

---

### get_features

Get mate features in the assembly.

```python
assemblies.get_features(did: str, wvm: str, wvm_id: str, eid: str) -> list[MateFeature]
```

```python
mates = client.assemblies.get_features(did, "w", wid, eid)
for m in mates:
    print(f"{m.name} ({m.mate_type}) — suppressed={m.suppressed}")
```

---

### get_occurrences

List all part occurrences with their 4×4 transform matrices.

```python
assemblies.get_occurrences(did: str, wvm: str, wvm_id: str, eid: str) -> list[Occurrence]
```

```python
occs = client.assemblies.get_occurrences(did, "w", wid, eid)
for occ in occs:
    print(f"Path: {occ.path}, Hidden: {occ.hidden}")
    print(f"  Transform: {occ.transform[:3]}...")  # First 3 of 16 values
```

**Example response object:**

```json
{
  "path": ["MR0abc123"],
  "hidden": false,
  "transform": [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]
}
```

---

### insert_instance

Insert a part or sub-assembly into the assembly (workspace only).

```python
assemblies.insert_instance(
    did: str, wid: str, eid: str,
    document_id: str, element_id: str, part_id: str,
    version_id: str | None = None,
    is_assembly: bool = False
) -> dict
```

```python
result = client.assemblies.insert_instance(
    did, wid, eid,
    document_id="804d...",
    element_id="5886...",
    part_id="JHD",
)
```

---

### transform_occurrences

Apply a 4×4 transform matrix to one or more occurrences.

```python
assemblies.transform_occurrences(
    did: str, wid: str, eid: str,
    transforms: list[dict]
) -> dict
```

Each transform dict should have `path` (list of occurrence IDs) and `transform` (16-element list representing a 4×4 matrix in row-major order).

```python
# Move an occurrence 10mm in X
client.assemblies.transform_occurrences(did, wid, eid, [
    {
        "path": ["MR0abc123"],
        "transform": [1,0,0,0.01, 0,1,0,0, 0,0,1,0, 0,0,0,1],
        "isRelative": True,
    }
])
```

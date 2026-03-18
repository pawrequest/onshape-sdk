---
sidebar_position: 4
title: PartStudiosApi
---

# PartStudiosApi

Interact with Part Studio features, variables, configuration, FeatureScript evaluation, and direct binary exports.

```python
ps_api = client.part_studios
```

**Base path:** `/api/v6/partstudios`

## Methods

### get_features

Get the feature tree of a Part Studio.

```python
part_studios.get_features(did: str, wvm: str, wvm_id: str, eid: str) -> list[Feature]
```

```python
features = client.part_studios.get_features(did, "w", wid, eid)
for f in features:
    print(f"{f.name} ({f.feature_type}) — suppressed={f.suppressed}")
```

**Example response object:**

```json
{
  "id": "FeatId1234",
  "name": "Extrude 1",
  "feature_type": "newBodySheetMetal",
  "suppressed": false,
  "parameters": [
    {"id": "depth", "type": "QUANTITY", "value": "0.01 meter"}
  ]
}
```

---

### add_feature

Add a new feature to a Part Studio (workspace only).

```python
part_studios.add_feature(did: str, wid: str, eid: str, feature: dict) -> dict
```

```python
result = client.part_studios.add_feature(did, wid, eid, {
    "type": 134,
    "typeName": "BTMFeature",
    "name": "My Sketch",
    "parameters": [ ... ]
})
```

---

### update_feature

Update an existing feature.

```python
part_studios.update_feature(did: str, wid: str, eid: str, feature_id: str, feature: dict) -> dict
```

---

### delete_feature

Delete a feature from the feature tree.

```python
part_studios.delete_feature(did: str, wid: str, eid: str, feature_id: str) -> None
```

---

### get_variables

Get all variables defined in a Part Studio.

```python
part_studios.get_variables(did: str, wvm: str, wvm_id: str, eid: str) -> list[Variable]
```

```python
variables = client.part_studios.get_variables(did, "w", wid, eid)
for v in variables:
    print(f"{v.name} = {v.value} ({v.expression})")
```

**Example response object:**

```json
{
  "name": "width",
  "value": 0.05,
  "expression": "50 mm",
  "description": "Bracket width"
}
```

---

### set_variables

Set variable values in a Part Studio (workspace only).

```python
part_studios.set_variables(did: str, wid: str, eid: str, variables: list[dict]) -> dict
```

```python
client.part_studios.set_variables(did, wid, eid, [
    {"name": "width", "expression": "60 mm"},
    {"name": "height", "expression": "25 mm"},
])
```

---

### get_configuration

Get the configuration definition for a Part Studio.

```python
part_studios.get_configuration(did: str, wvm: str, wvm_id: str, eid: str) -> dict
```

---

### evaluate_featurescript

Evaluate a FeatureScript expression in the Part Studio context.

```python
part_studios.evaluate_featurescript(
    did: str, wvm: str, wvm_id: str, eid: str,
    script: str, queries: dict | None = None
) -> dict
```

```python
result = client.part_studios.evaluate_featurescript(
    did, "w", wid, eid,
    script='function(context is Context, queries is map) { return evLength(context, {"entities": qEverything()}); }'
)
print(result)
```

---

### export_stl

Export Part Studio as STL (binary).

```python
part_studios.export_stl(
    did: str, wvm: str, wvm_id: str, eid: str,
    part_ids: list[str] | None = None,
    mode: str = "binary",
    units: str = "millimeter",
    angle_tolerance: float = 0.1090830782496456,
    chord_tolerance: float = 0.01
) -> bytes
```

```python
stl_data = client.part_studios.export_stl(did, "w", wid, eid)
with open("output.stl", "wb") as f:
    f.write(stl_data)
```

---

### export_parasolid

Export Part Studio as Parasolid (.x_t).

```python
part_studios.export_parasolid(
    did: str, wvm: str, wvm_id: str, eid: str,
    part_ids: list[str] | None = None,
    version: str = "35.1"
) -> bytes
```

```python
data = client.part_studios.export_parasolid(did, "w", wid, eid)
with open("output.x_t", "wb") as f:
    f.write(data)
```

---

### export_dxf

Export Part Studio as DXF (binary).

```python
part_studios.export_dxf(
    did: str, wvm: str, wvm_id: str, eid: str,
    part_ids: list[str] | None = None
) -> bytes
```

```python
dxf_data = client.part_studios.export_dxf(did, "w", wid, eid)
with open("output.dxf", "wb") as f:
    f.write(dxf_data)
```

:::tip STL vs Translation API
These direct export methods are simpler but limited to Part Studio elements. For assemblies or more format options (STEP, IGES, etc.), use the [TranslationsApi](./translations).
:::

---
sidebar_position: 100
title: Type Reference
---

# Type Reference

All API responses are parsed into typed Python dataclasses. Every dataclass has a `from_dict(data)` classmethod and a `.raw` attribute containing the full API response dict.

```python
from onshape_sdk import Document, Part, TranslationStatus  # etc.
```

## Dataclass Reference

| Class | Key Fields | Used By |
|-------|------------|---------|
| `PaginatedList[T]` | `items`, `next`, `previous`, `href` | Internal pagination |
| `UserInfo` | `id`, `name`, `email`, `company_name`, `image` | `test_auth()` |
| `Owner` | `id`, `name`, `type` | `Document` |
| `Workspace` | `id`, `name`, `description` | `documents.get_workspaces()` |
| `DocumentVersion` | `id`, `name`, `description`, `created_at`, `creator` | `documents.get_versions()` |
| `Document` | `id`, `name`, `owner`, `created_at`, `modified_at`, `default_workspace_id` | `documents.*` |
| `Element` | `id`, `name`, `element_type`, `data_type` | `documents.get_elements()` |
| `Part` | `name`, `part_id`, `body_type`, `material`, `appearance` | `parts.*` |
| `FeatureParameter` | `id`, `type`, `value` | `Feature` |
| `Feature` | `id`, `name`, `feature_type`, `suppressed`, `parameters` | `part_studios.get_features()` |
| `Variable` | `name`, `value`, `expression`, `description` | `part_studios.get_variables()` |
| `Occurrence` | `path`, `hidden`, `transform` | `assemblies.get_occurrences()` |
| `BomRow` | `item_name`, `quantity`, `item_source` | `BomTable` |
| `BomTable` | `headers`, `rows` | `assemblies.get_bom()` |
| `MateFeature` | `id`, `name`, `mate_type`, `suppressed` | `assemblies.get_features()` |
| `AssemblyDefinition` | `root_parts`, `parts`, `sub_assemblies` | `assemblies.get_definition()` |
| `DrawingView` | `id`, `name`, `view_type`, `scale` | `drawings.get_views()` |
| `TranslationStatus` | `id`, `request_state`, `result_external_data_ids`, `failure_reason`, `name` | `translations.*` |
| `MetadataProperty` | `name`, `property_id`, `value`, `value_type` | `metadata.*` |
| `ThumbnailSize` | `size`, `href` | `ThumbnailInfo` |
| `ThumbnailInfo` | `sizes` | `thumbnails.get_info()` |
| `Webhook` | `id`, `url`, `events`, `options` | `webhooks.*` |

## Common Patterns

### Accessing Raw Data

Every dataclass exposes the full API response via `.raw`:

```python
doc = client.documents.get(did)
print(doc.name)            # Typed field
print(doc.raw["createdBy"])  # Access any field from the raw API response
```

### from_dict Pattern

All types use the same factory pattern:

```python
data = {"id": "abc", "name": "Test", ...}
doc = Document.from_dict(data)
```

This makes it easy to construct types from custom API calls:

```python
resp = client.get("/api/v6/documents/abc123")
doc = Document.from_dict(resp.json())
```

### TranslationStatus Helpers

`TranslationStatus` has convenience properties for polling:

```python
status = client.translations.get_status(job_id)
status.is_done    # True if request_state == "DONE"
status.is_failed  # True if request_state == "FAILED"
status.is_active  # True if request_state == "ACTIVE"
```

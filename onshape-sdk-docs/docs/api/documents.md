---
sidebar_position: 2
title: DocumentsApi
---

# DocumentsApi

Manage Onshape documents — list, search, create, version, and delete.

```python
docs_api = client.documents
```

**Base path:** `/api/v6/documents`

## Methods

### list

List documents accessible to the current user.

```python
documents.list(
    owner_type: str = "1",
    limit: int = 20,
    offset: int = 0,
    sort_column: str = "modifiedAt",
    sort_order: str = "desc"
) -> list[Document]
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `owner_type` | `str` | `"1"` | `"0"` = own, `"1"` = own + shared, `"4"` = company |
| `limit` | `int` | `20` | Max results per page |
| `offset` | `int` | `0` | Pagination offset |
| `sort_column` | `str` | `"modifiedAt"` | Sort field |
| `sort_order` | `str` | `"desc"` | `"asc"` or `"desc"` |

```python
docs = client.documents.list(limit=5)
for doc in docs:
    print(f"{doc.name} — modified {doc.modified_at}")
```

**Example response object:**

```json
{
  "id": "804d1a7a071db077dbad4e42",
  "name": "My CAD Project",
  "owner": {"id": "abc123", "name": "Zach", "type": "1"},
  "created_at": "2026-01-15T10:30:00Z",
  "modified_at": "2026-03-17T14:22:00Z",
  "default_workspace_id": "c9f128ed004c27e492b8cebb"
}
```

---

### get

Get a single document by ID.

```python
documents.get(did: str) -> Document
```

```python
doc = client.documents.get("804d1a7a071db077dbad4e42")
print(doc.name, doc.default_workspace_id)
```

---

### search

Full-text search across document names and descriptions.

```python
documents.search(
    query: str,
    limit: int = 20,
    offset: int = 0
) -> list[Document]
```

```python
results = client.documents.search("bracket")
for doc in results:
    print(doc.name)
```

---

### get_elements

List all elements (tabs) in a document.

```python
documents.get_elements(
    did: str,
    wvm: str,
    wvm_id: str
) -> list[Element]
```

```python
elements = client.documents.get_elements(did, "w", wid)
for el in elements:
    print(f"{el.name} ({el.element_type})")
    # e.g., "Part Studio 1 (PARTSTUDIO)"
```

**Example response object:**

```json
{
  "id": "58863216bdaab008805f5f3f",
  "name": "Part Studio 1",
  "element_type": "PARTSTUDIO",
  "data_type": "onshape-app/partstudio"
}
```

---

### get_versions

List all named versions of a document.

```python
documents.get_versions(did: str) -> list[DocumentVersion]
```

```python
versions = client.documents.get_versions(did)
for v in versions:
    print(f"v{v.name}: {v.id} — {v.description}")
```

---

### get_workspaces

List all workspaces (branches) in a document.

```python
documents.get_workspaces(did: str) -> list[Workspace]
```

```python
workspaces = client.documents.get_workspaces(did)
for ws in workspaces:
    print(f"{ws.name}: {ws.id}")
```

---

### create

Create a new empty document.

```python
documents.create(
    name: str,
    description: str = "",
    owner_id: str | None = None,
    owner_type: int = 1,
    is_public: bool = False
) -> Document
```

```python
new_doc = client.documents.create(
    name="My New Project",
    description="Created via SDK",
    is_public=False,
)
print(new_doc.id)
```

---

### create_version

Create a named version (snapshot) of a document.

```python
documents.create_version(
    did: str,
    wid: str,
    name: str,
    description: str = ""
) -> DocumentVersion
```

```python
version = client.documents.create_version(
    did, wid, name="v1.0", description="First release"
)
print(version.id)
```

---

### delete

Delete a document (moves to trash by default).

```python
documents.delete(did: str, forever: bool = False) -> None
```

```python
# Move to trash
client.documents.delete(did)

# Permanent delete
client.documents.delete(did, forever=True)
```

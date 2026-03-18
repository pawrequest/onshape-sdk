---
sidebar_position: 1
title: OnshapeClient
---

# OnshapeClient

The core client that handles authentication and provides access to all API resources.

```python
from onshape_sdk import OnshapeClient
```

## Constructor

```python
OnshapeClient(access_key: str, secret_key: str, base_url: str = "https://cad.onshape.com")
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `access_key` | `str` | *required* | Onshape API access key |
| `secret_key` | `str` | *required* | Onshape API secret key |
| `base_url` | `str` | `"https://cad.onshape.com"` | Base URL (change for Enterprise) |

## Class Methods

### from_env

```python
OnshapeClient.from_env(
    base_url: str = "https://cad.onshape.com",
    dotenv_path: str | None = None
) -> OnshapeClient
```

Creates a client using environment variables `ONSHAPE_ACCESS_KEY` and `ONSHAPE_SECRET_KEY`. Automatically loads `.env` files via `python-dotenv`.

```python
# Uses .env in current directory
client = OnshapeClient.from_env()

# Custom .env path
client = OnshapeClient.from_env(dotenv_path="/path/to/.env")

# Enterprise instance
client = OnshapeClient.from_env(base_url="https://mycompany.onshape.com")
```

## Instance Methods

### test_auth

```python
client.test_auth() -> dict
```

Runs a diagnostic against two endpoints to verify credentials are valid.

```python
result = client.test_auth()
print(result)
```

**Response:**

```json
{
  "user": "Zach Sharma (zach@example.com)",
  "documents_accessible": 42
}
```

### get

```python
client.get(path: str, query_params: dict = None, accept: str = "application/json") -> requests.Response
```

Authenticated GET request. Returns the raw `requests.Response`.

```python
resp = client.get("/api/v6/documents", {"limit": 5})
data = resp.json()
```

### post

```python
client.post(path: str, body: dict = None, query_params: dict = None) -> requests.Response
```

Authenticated POST with JSON body.

### put

```python
client.put(path: str, body: dict = None, query_params: dict = None) -> requests.Response
```

Authenticated PUT with JSON body.

### delete

```python
client.delete(path: str, query_params: dict = None) -> requests.Response
```

Authenticated DELETE request.

## Resource Properties

All resource APIs are lazy-loaded via `@cached_property`:

| Property | Type | Description |
|----------|------|-------------|
| `client.documents` | [`DocumentsApi`](./documents) | Document CRUD, search, versions |
| `client.parts` | [`PartsApi`](./parts) | Part listing, mass properties, bounding boxes |
| `client.part_studios` | [`PartStudiosApi`](./part-studios) | Features, variables, STL/DXF export |
| `client.assemblies` | [`AssembliesApi`](./assemblies) | Assembly definition, BOM, mates |
| `client.translations` | [`TranslationsApi`](./translations) | Async CAD export/import |
| `client.drawings` | [`DrawingsApi`](./drawings) | Drawing views and geometry |
| `client.blob_elements` | [`BlobElementsApi`](./blob-elements) | File upload/download |
| `client.metadata` | [`MetadataApi`](./metadata) | Custom metadata properties |
| `client.thumbnails` | [`ThumbnailsApi`](./thumbnails) | Thumbnail images |
| `client.webhooks` | [`WebhooksApi`](./webhooks) | Webhook management |

```python
# All resource APIs are accessed as properties
parts = client.parts.list(did, "w", wid, eid)
doc = client.documents.get(did)
bom = client.assemblies.get_bom(did, "w", wid, eid)
```

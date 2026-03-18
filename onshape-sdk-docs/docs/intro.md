---
slug: /
sidebar_position: 1
title: Getting Started
---

# Onshape Python SDK

A lightweight, fully-typed Python SDK for the Onshape REST API. Provides HMAC-SHA256 authentication, typed dataclasses for all responses, and high-level helpers for common workflows like CAD export.

## Quick Start

```python
from onshape_sdk import OnshapeClient, parse_onshape_url

# Create client from .env file (ONSHAPE_ACCESS_KEY, ONSHAPE_SECRET_KEY)
client = OnshapeClient.from_env()

# Verify authentication
client.test_auth()

# Parse an Onshape document URL
ids = parse_onshape_url("https://cad.onshape.com/documents/abc123/w/def456/e/789fed")

# List all parts in a Part Studio
parts = client.parts.list(ids["did"], ids["wvm_type"], ids["wvm_id"], ids["eid"])
for part in parts:
    print(f"{part.name} ({part.part_id})")

# Export a DXF using the high-level translation helper
client.translations.export(
    did=ids["did"],
    wvm=ids["wvm_type"],
    wvm_id=ids["wvm_id"],
    eid=ids["eid"],
    format_name="DXF",
    output_path="output.dxf",
    verbose=True,
)
```

## Features

- **HMAC-SHA256 authentication** — handles nonce generation, signing strings, and header construction
- **22 typed dataclasses** — every API response is parsed into Python objects with `from_dict()` classmethods
- **10 resource API modules** — Documents, Parts, Part Studios, Assemblies, Translations, Drawings, Blob Elements, Metadata, Thumbnails, Webhooks
- **High-level helpers** — one-call DXF/STL/STEP export with automatic polling
- **Environment variable config** — load credentials from `.env` with `from_env()`

## Requirements

- Python 3.8+
- `requests`
- `python-dotenv`

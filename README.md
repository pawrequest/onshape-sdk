# onshape-sdk-zachsharma

A lightweight, typed Python SDK for the [Onshape REST API](https://onshape-public.github.io/docs/).

Documentation: [https://zachariah-sharma.github.io/pyshape/](https://zachariah-sharma.github.io/pyshape/)

## Install

```bash
pip install onshape-sdk-zachsharma
```

## Quick start

```python
from onshape_sdk import OnshapeClient, parse_onshape_url

client = OnshapeClient.from_env()
ids = parse_onshape_url("https://cad.onshape.com/documents/.../w/.../e/...")

bom = client.assemblies.get_bom(ids["did"], ids["wvm_type"], ids["wvm_id"], ids["eid"])
for row in bom.rows:
    print(row.part_number, row.name, row.quantity, row.material_name)
```

## Authentication

Create Onshape API keys and add them to a `.env` file:

```env
ONSHAPE_ACCESS_KEY=your_access_key
ONSHAPE_SECRET_KEY=your_secret_key
```

## License

MIT

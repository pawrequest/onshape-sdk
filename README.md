# onshape-sdk-pawrequest

A lightweight, typed Python SDK for the [Onshape REST API](https://onshape-public.github.io/docs/).

Upstream Documentation: [https://zachariahsharma.github.io/onshape-sdk/](https://zachariahsharma.github.io/onshape-sdk/)

Upstream didn't work for some routes and it's api_version is old, so i forked.

I have not tested all routes, ymmv.

Major Fork changes:

- Updated API version from 6 to 10
- Fixed some broken routes
- Added pydantic-settings
- Changed the auth setup. (`onshape_sdk.auth.OnshapeHmacAuth`)
- uv native

## Install

```bash
uv tool install onshape-sdk-pr
```

## Usage

```bash
onshape-sdk --help
```

or don't install and run from uv cache:

```bash
uv tool run --from onshape-sdk-pr onshape-sdk --help
```


### Configuration

Create Onshape API access and secret keys via the developer portal on OnShape's website.

PydanticSettings are built from .env file or environment variables.  
Place a .env with required inputs in default location `./.env` (sibling of this readme).

Or do one of:

- Pass custom .env locations to `OnshapeSettings(_env_file="config/onshape.env")`,
- Set the required inputs in your environment,
- Instantiate `OnshapeSettings` with the required inputs.

#### required inputs

ONSHAPE_ACCESS_KEY=your_access_key  
ONSHAPE_SECRET_KEY=your_secret_key

## Usage

### cli

cli entry is via uv from `src/main.py` - see there for details.  
uv sets `onshape-sdk` as the program name
Run `onshape-sdk --help` to see available commands.

atm i mostly use this project as an exporter to speed up iterating from onshape to slicer.

Commands:

- Export

```bash
onshape-sdk export -u <onshape partstudio url> -o 'exported parts.stl'
```

Add `-pf <Part name>` to filter by part name.
On Windows, add `-l` to open the exported file in the default app, i.e slicer.

### python


```python
from onshape_sdk import OnshapeClient, OnshapeIdsTup, OnshapeSettings

settings = OnshapeSettings()  # optional - otherwise read default .env location or env_vars 
client = OnshapeClient(settings)  # or just `OnshapeClient() for defaults`
url = 'https://cad.onshape.com/documents/804d1a7a071db077dbad4e42/w/c9f128ed004c27e492b8cebb/e/58863216bdaab008805f5f3f'
ids = OnshapeIdsTup.from_url(url)
bom = client.assemblies.get_bom(*ids)
for row in bom.rows:
    print(row.part_number, row.name, row.quantity, row.material_name)
```

## License

MIT

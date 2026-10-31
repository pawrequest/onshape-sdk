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

## Install

```
git clone <rep-url>
```

or don't and use uv:

```shell
uv tool run --from git+https://github.com/pawrequest/onshape-sdk onshape-sdk export
```

### Configuration

Create Onshape API access and secret keys via the developer portal on OnShape's website.

PydanticSettings are built from .env file or environment variables.  
Place a .env with required inputs in default location "<project_root>/.env"  (sibling of this readme)  
Or do one of:

- Pass custom .env locations to `OnshapeSettings(_env_file=<path_to_env_file>)`,
- Set the required inputs in your environment,
- Instantiate `OnshapeSettings` with the required inputs.

#### required inputs

ONSHAPE_ACCESS_KEY=your_access_key  
ONSHAPE_SECRET_KEY=your_secret_key

## Usage

### cli

cli entry is via uv from `src/main.py` - see there fore details.  
uv sets `onshape-sdk` as the program name
`onshape-sdk <command> <command options>`  
atm i mostly use this project as an exporter to speed up iterating from onshape to slicer.

Commands:

- Export

```
onshape-sdk export /
    -u <url-to-partstudio> /
    -o <optional output file or dir> /  # save exported stl bytes
    -pf <optional part-name filter>

```

### python

```python
from src.onshape_sdk import OnshapeClient, OnshapeIdsTup, OnshapeSettings

settings = OnshapeSettings()  # optional - otherwise read default .env location or env_vars 
client = OnshapeClient(settings)  # or just `OnshapeClient() for defaults`
url = '<ONSHAPE_URL>'
ids = OnshapeIdsTup.from_url(url)
bom = client.assemblies.get_bom(*ids)
for row in bom.rows:
    print(row.part_number, row.name, row.quantity, row.material_name)
```

## License

MIT

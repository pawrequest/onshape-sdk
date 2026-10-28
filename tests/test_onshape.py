import os
from pathlib import Path
from pprint import pprint

import pytest
from dotenv import load_dotenv

from onshape_sdk import AssemblyDefinition, OnshapeClient, Part
from onshape_sdk.ids import OnshapeIdsTup
from onshape_sdk.client_routines import export_from_ps, get_parts_by_name

env = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env, override=True)


def ids_from_env(key: str) -> OnshapeIdsTup:
    url = os.environ.get(key)
    if not url:
        raise ValueError(f'{key} environment variable is not set')
    ids = OnshapeIdsTup.from_url(url)
    return ids


@pytest.fixture
def path_ids_assy():
    ids = ids_from_env('ONSHAPE_TEST_URL_ASSY')
    return ids


@pytest.fixture
def path_ids_parts():
    ids = ids_from_env('ONSHAPE_TEST_URL_PART')
    return ids


@pytest.fixture
def client() -> OnshapeClient:
    return OnshapeClient()


@pytest.fixture(autouse=True)
def capsys_out(capsys):
    yield
    with capsys.disabled():
        stdout = capsys.readouterr().out
        print(stdout)


def test_auth(client):
    res = client.test_auth()
    print(res)
    assert res is True


def test_assy_def(client, path_ids_assy):
    res = client.assemblies.get_definition(*path_ids_assy)
    assert isinstance(res, AssemblyDefinition)
    assert isinstance(res.root_assembly, dict)


def test_get_part_by_name(client, path_ids_parts):
    parts = client.parts.list(*path_ids_parts)
    print('ALL PARTS:')
    pprint(parts)
    assert all(isinstance(part, Part) for part in parts)
    filtered = get_parts_by_name(client, path_ids_parts)
    print('FILTERED PARTS:')
    pprint(filtered)
    assert len(parts) >  len(filtered) >  0


def test_export_stl(client, path_ids_parts):
    result = export_from_ps(client, path_ids_parts, Path('.'), filter_text='test')
    assert result

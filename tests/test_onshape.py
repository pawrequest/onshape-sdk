import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

from onshape_sdk import OnshapeClient
from onshape_sdk.ids import OnshapeIdsTup

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
    # with capsys.disabled():
    #     stdout = capsys.readouterr().out
    #     print(stdout)


def test_assy_def(client, path_ids_assy):
    res = client.assemblies.get_definition(*path_ids_assy)
    print(res.root_assembly)


def get_part_by_name(client, path_ids_parts, search_text = 'test'):
    parts = client.parts.list(*path_ids_parts)
    filtered = [_ for _ in parts if search_text.lower() in _.name.lower()]
    ...
    return filtered


def test_get_part_by_name(client, path_ids_parts):
    parts = get_part_by_name(client, path_ids_parts)
    print(parts)
    ...


def test_export_stl(client, path_ids_parts):
    result = client.part_studios.export_stl(*path_ids_parts, part_ids='')
    with open('ONHAPE_TEST.stl', 'wb') as f:
        f.write(result)

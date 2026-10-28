import os

import pytest

from onshape_sdk import OnshapeClient, OnshapeIds, parse_onshape_url


@pytest.fixture
def ids_from_env() -> OnshapeIds:
    url = os.environ.get('ONSHAPE_TEST_URL')
    if not url:
        raise ValueError('ONSHAPE_TEST_URL environment variable is not set')
    ids = parse_onshape_url(url)
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


def test_auth(capsys, client):
    res = client.test_auth()
    print(res)
    assert res is True
    # with capsys.disabled():
    #     stdout = capsys.readouterr().out
    #     print(stdout)


def test_assy_def(client, ids_from_env):
    res = client.assemblies.get_definition(*list(ids_from_env.values()))
    print(res.root_assembly)
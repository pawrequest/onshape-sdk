import base64
import hmac
import secrets
import string
from collections.abc import Generator
from email.utils import formatdate
from functools import cached_property
from pathlib import Path

import httpx
from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from onshape_sdk.utils import PROJECT_ROOT

_NONCE_CHARS = string.ascii_letters + string.digits


def default_headers() -> dict[str, str]:
    """Return default headers for Onshape API requests."""
    return {
        'Accept': 'application/json;charset=UTF-8; qs=0.09',
        'Content-Type': 'application/json;charset=UTF-8; qs=0.09',
    }


class OnshapeSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / '.env',
        env_file_encoding='utf-8',
    )
    access_key: SecretStr = Field(..., alias='ONSHAPE_ACCESS_KEY')
    secret_key: SecretStr = Field(..., alias='ONSHAPE_SECRET_KEY')
    api_version: str = 'v10'
    root_url: str = Field('https://cad.onshape.com/api', alias='ONSHAPE_BASE_URL')
    headers: dict = Field(default_factory=default_headers)
    max_retries: int = 3
    onshape_test_url_assy: Path | None = None
    onshape_test_url_part: Path | None = None

    def auth(self):
        return OnshapeHmacAuth(self.access_key, self.secret_key)

    @cached_property
    def base_url(self):
        return f'{self.root_url}/{self.api_version}'



class SecretBasicAuth(httpx.Auth):
    def __init__(self, username: SecretStr, password: SecretStr) -> None:
        self._username = username
        self._password = password

    def auth_flow(self, request: httpx.Request):
        # unwrapped per request, never stored as plain str on self
        basic = httpx.BasicAuth(
            self._username.get_secret_value(),
            self._password.get_secret_value(),
        )
        yield from basic.auth_flow(request)

    def __repr__(self) -> str:
        return f'{type(self).__name__}(<redacted>)'


class OnshapeHmacAuth(httpx.Auth):
    def __init__(self, access_key: SecretStr, secret_key: SecretStr) -> None:
        self._access = access_key
        self._secret = secret_key

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        nonce = ''.join(secrets.choice(_NONCE_CHARS) for _ in range(25))
        date = formatdate(usegmt=True)
        content_type = request.headers.get('content-type', 'application/json')
        path = request.url.raw_path.split(b'?', 1)[0].decode()
        query = request.url.query.decode()

        signing_string = (
            f'{request.method}\n{nonce}\n{date}\n{content_type}\n{path}\n{query}\n'
        ).lower()

        access = self._access.get_secret_value()
        digest = hmac.digest(
            self._secret.get_secret_value().encode(), signing_string.encode(), 'sha256'
        )
        sig = base64.b64encode(digest).decode()

        request.headers['Date'] = date
        request.headers['On-Nonce'] = nonce
        request.headers['Authorization'] = f'On {access}:HmacSHA256:{sig}'
        yield request

    def __repr__(self) -> str:
        return f'{type(self).__name__}(<redacted>)'

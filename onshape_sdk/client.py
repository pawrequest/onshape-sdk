"""Onshape API client with HMAC-SHA256 authentication.

Authentication reference:
    https://onshape-public.github.io/docs/auth/apikeys/

Authorization header format:
    ``On <AccessKey>:HmacSHA256:<Signature>``

The nonce goes ONLY in the ``On-Nonce`` header — never in the Authorization
string.  The full signing string is lowercased before hashing.
"""

from __future__ import annotations

from functools import cached_property
from typing import Optional
from urllib.parse import urlencode

import httpx

# import requests

from onshape_sdk.api_version import API_VERSION_PATH
from onshape_sdk.auth import OnshapeSettings


class OnshapeClient:
    """Lightweight Onshape REST API client using API-key HMAC auth via httpx."""

    def __init__(
        self,
        settings: OnshapeSettings | None = None,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        settings = settings or OnshapeSettings()
        self.settings = settings
        self.base_url = settings.base_url.rstrip('/')
        self.http = httpx.Client(
            base_url=self.settings.base_url,
            auth=(settings.auth()),
            headers=self.settings.headers,
            timeout=30,
            transport=transport,
        )

    # ── HTTP verbs ────────────────────────────────────────────────────────────

    def get(
        self,
        path: str,
        query_params: Optional[dict] = None,
        accept: str = 'application/json',
    ) -> httpx.Response:
        """Authenticated GET request."""
        headers = self.settings.headers
        headers['Accept'] = accept
        return self.http.get(path, headers=headers, params=query_params)

    def post(
        self,
        path: str,
        body: Optional[dict | list] = None,
        query_params: Optional[dict] = None,
    ) -> httpx.Response:
        """Authenticated POST request (JSON body)."""
        url = self.base_url + path
        if query_params:
            url += '?' + urlencode(query_params)
        return self.http.post(url, json=body if body is not None else {})

    def put(
        self,
        path: str,
        body: Optional[dict | list] = None,
        query_params: Optional[dict] = None,
    ) -> httpx.Response:
        """Authenticated PUT request (JSON body)."""
        url = self.base_url + path
        return self.http.put(url, params=query_params, json=body if body is not None else {})

    def delete(
        self,
        path: str,
        query_params: Optional[dict] = None,
    ) -> httpx.Response:
        """Authenticated DELETE request."""
        return self.http.delete(path, params=query_params)

    # ── Resource APIs ─────────────────────────────────────────────────────────
    # Lazily instantiated via cached_property so they're only created once.

    @cached_property
    def documents(self):
        """Documents API — create, list, search, version."""
        from .documents import DocumentsApi

        return DocumentsApi(self)

    @cached_property
    def parts(self):
        """Parts API — list and inspect parts."""
        from .parts import PartsApi

        return PartsApi(self)

    @cached_property
    def part_studios(self):
        """Part Studios API — features, variables, direct exports."""
        from .part_studios import PartStudiosApi

        return PartStudiosApi(self)

    @cached_property
    def assemblies(self):
        """Assemblies API — definitions, BOM, mates, occurrences."""
        from .assemblies import AssembliesApi

        return AssembliesApi(self)

    @cached_property
    def drawings(self):
        """Drawings API — views and geometry."""
        from .drawings import DrawingsApi

        return DrawingsApi(self)

    @cached_property
    def translations(self):
        """Translations API — async export/import engine."""
        from .translations import TranslationsApi

        return TranslationsApi(self)

    @cached_property
    def blob_elements(self):
        """Blob Elements API — upload and download files."""
        from .blob_elements import BlobElementsApi

        return BlobElementsApi(self)

    @cached_property
    def metadata(self):
        """Metadata API — custom properties on elements and parts."""
        from .metadata import MetadataApi

        return MetadataApi(self)

    @cached_property
    def thumbnails(self):
        """Thumbnails API — preview images."""
        from .thumbnails import ThumbnailsApi

        return ThumbnailsApi(self)

    @cached_property
    def webhooks(self):
        """Webhooks API — event-driven notifications."""
        from .webhooks import WebhooksApi

        return WebhooksApi(self)

    # ── Diagnostics ───────────────────────────────────────────────────────────

    def test_auth(self) -> bool:
        """Run a quick auth diagnostic and print results.

        Tests:
            1. ``GET /{API_VERSION_PATH}/users/sessioninfo`` — verifies HMAC signing works
            2. ``GET /{API_VERSION_PATH}/documents?limit=1``  — verifies read scope

        Returns
        -------
        bool
            ``True`` if all tests pass.
        """
        sep = '─' * 50
        all_ok = True

        print(sep)
        print('Onshape Auth Diagnostic')
        print(sep)
        print(f'  Access Key : {self.settings.access_key.get_secret_value()[:8]}…')
        print(f'  Base URL   : {self.base_url}')

        # Test 1 — session info
        print(f'\n  [1/2] GET /{API_VERSION_PATH}/users/sessioninfo')
        r1 = self.get('{API_VERSION_PATH}/users/sessioninfo')
        if r1.status_code == 200:
            me = r1.json()
            print(f'    ✅ Authenticated as: {me.get("name")} ({me.get("email")})')
        else:
            all_ok = False
            print(f'    ❌ {r1.status_code} — {self._err(r1)}')
            if r1.status_code == 401:
                print(
                    '    → ACCESS_KEY or SECRET_KEY is wrong — regenerate at dev-portal.onshape.com'
                )
            elif r1.status_code == 204:
                print('    → 204 No Content — keys may be invalid or expired')

        # Test 2 — list documents
        print(f'\n  [2/2] GET /{API_VERSION_PATH}/documents?limit=1')
        r2 = self.get(f'{API_VERSION_PATH}/documents', query_params={'filter': 0, 'limit': 1})
        if r2.status_code == 200:
            items = r2.json().get('items', [])
            print(f'    ✅ Read scope OK — found {len(items)} document(s)')
        else:
            all_ok = False
            print(f'    ❌ {r2.status_code} — {self._err(r2)}')
            if r2.status_code == 403:
                print('    → API key may be missing read permissions')

        print(f'\n{sep}')
        print(f'  Result: {"✅ All good!" if all_ok else "❌ See errors above."}')
        print(sep)
        return all_ok

    @staticmethod
    def _err(resp: httpx.Response) -> str:
        try:
            return resp.json().get('message', resp.text[:200])
        except Exception:
            return resp.text[:200]

    # ── repr ──────────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return f"OnshapeClient(access_key='{self.settings.access_key.get_secret_value()[:8]}…', base_url='{self.base_url}')"

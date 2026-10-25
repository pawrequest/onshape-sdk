"""Drawings API — views and export helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .types import DrawingView
from .utils import build_wvm_path

if TYPE_CHECKING:
    from .client import OnshapeClient


class DrawingsApi:
    """Endpoints under ``/api/v10/drawings``."""

    _BASE = "/api/v10/drawings"

    def __init__(self, client: "OnshapeClient") -> None:
        self._c = client

    def _path(self, did: str, wvm: str, wvm_id: str, eid: str) -> str:
        return f"{self._BASE}{build_wvm_path(did, wvm, wvm_id, eid)}"

    def get(
        self,
        did: str,
        wvm: str,
        wvm_id: str,
        eid: str,
    ) -> dict[str, Any]:
        """Get drawing element metadata."""
        r = self._c.get(self._path(did, wvm, wvm_id, eid))
        r.raise_for_status()
        return r.json()

    def get_views(
        self,
        did: str,
        wvm: str,
        wvm_id: str,
        eid: str,
    ) -> list[DrawingView]:
        """List all views in the drawing."""
        r = self._c.get(f"{self._path(did, wvm, wvm_id, eid)}/views")
        r.raise_for_status()
        data = r.json()
        items = data if isinstance(data, list) else data.get("views", [])
        return [DrawingView.from_dict(v) for v in items if isinstance(v, dict)]

    def get_view_geometry(
        self,
        did: str,
        wvm: str,
        wvm_id: str,
        eid: str,
        view_id: str,
    ) -> dict[str, Any]:
        """Get the JSON geometry for a specific drawing view."""
        r = self._c.get(
            f"{self._path(did, wvm, wvm_id, eid)}/views/{view_id}/jsongeometry"
        )
        r.raise_for_status()
        return r.json()

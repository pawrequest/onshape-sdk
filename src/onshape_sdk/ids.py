from typing import NamedTuple

from .utils import parse_onshape_url, build_wvm_path


class OnshapeIdsTup(NamedTuple):
    """IDs parsed from an Onshape document URL."""

    did: str  # document ID
    wvm_type: str  # 'w' (workspace), 'v' (version), or 'm' (microversion)
    wvm_id: str  # workspace / version / microversion ID
    eid: str | None = None  # element ID

    @classmethod
    def from_url(cls, url: str) -> 'OnshapeIdsTup':
        parsed = parse_onshape_url(url)
        return cls(**parsed)

    def build_path(self):
        return build_wvm_path(*self)

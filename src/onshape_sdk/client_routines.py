from pathlib import Path

from .types import Part
from .client import OnshapeClient
from .ids import OnshapeIdsTup
from .utils import filter_named, save_bytes


def get_parts_by_name(
    client: OnshapeClient, path_ids: OnshapeIdsTup, filter_text='test'
) -> list[Part]:
    parts = client.parts.list(*path_ids)
    filtered = filter_named(parts, filter_text)
    return filtered


def export_from_ps(
    client: OnshapeClient,
    path_ids: OnshapeIdsTup,
    save_path: Path | None = None,
    filter_text: str = '',
) -> bytes | Path:
    filtered = get_parts_by_name(client, path_ids, filter_text)
    part_ids = [part.part_id for part in filtered]
    print(f'Exporting {[_.name for _ in filtered]}')
    exported_bytes = client.part_studios.export_stl(*path_ids, part_ids=part_ids)
    if save_path:
        if save_path.is_dir():
            save_path = save_path / f'{filtered[0].name}.stl'
        save_bytes(exported_bytes, save_path)
        return save_path
    return exported_bytes

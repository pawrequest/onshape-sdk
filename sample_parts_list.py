"""
sample_parts_list.py

Gets all parts, their quantities, part numbers, and materials from an Onshape
assembly URL.

Usage:
    python sample_parts_list.py <onshape_assembly_url>

Example:
    python sample_parts_list.py "https://cad.onshape.com/documents/804d.../w/c9f1.../e/5886..."
"""

import sys

from onshape_sdk import OnshapeClient, parse_onshape_url
from onshape_sdk.auth import OnshapeSettings


def get_parts_list(url: str):
    settings = OnshapeSettings()
    client = OnshapeClient(settings=settings)
    ids = parse_onshape_url(url)
    did = ids["did"]
    wvm = ids["wvm_type"]
    wvm_id = ids["wvm_id"]
    eid = ids["eid"]

    print(f"\nFetching assembly data for document {did[:8]}...\n")

    bom = client.assemblies.get_bom(did, wvm, wvm_id, eid, indented=False)
    rows = [
        {
            "name": row.name or row.description or "Unnamed",
            "part_number": row.part_number or "—",
            "part_id": row.item_source.get("partId", "—") or "—",
            "qty": row.quantity or 1,
            "material": row.material_name,
        }
        for row in bom.rows
    ]

    if not rows:
        print("No parts found in this assembly.")
        return

    pn_w = max(len(r["part_number"]) for r in rows)
    name_w = max(len(r["name"]) for r in rows)
    mat_w  = max(len(r["material"]) for r in rows)
    pn_w = max(pn_w, 11)
    name_w = max(name_w, 4)   # min header width
    mat_w  = max(mat_w,  8)

    header = f"{'Part Number':<{pn_w}}  {'Part':<{name_w}}  {'Qty':>4}  {'Material':<{mat_w}}"
    sep    = "─" * len(header)
    print(sep)
    print(header)
    print(sep)
    for r in rows:
        print(
            f"{r['part_number']:<{pn_w}}  {r['name']:<{name_w}}  "
            f"{r['qty']:>4}  {r['material']:<{mat_w}}"
        )
    print(sep)
    print(f"Total BOM rows:     {len(rows)}")
    print(f"Total part count:   {sum(r['qty'] for r in rows)}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sample_parts_list.py <onshape_assembly_url>")
        sys.exit(1)

    get_parts_list(sys.argv[1])

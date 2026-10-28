from argparse import ArgumentParser, Namespace
from pathlib import Path

from onshape_sdk import OnshapeClient
from onshape_sdk.auth import OnshapeSettings
from onshape_sdk.client_routines import export_from_ps
from onshape_sdk.ids import OnshapeIdsTup
from onshape_sdk.utils import PROJECT_ROOT


def cmd_export(client: OnshapeClient, args: Namespace) -> None:
    ids = OnshapeIdsTup.from_url(url=args.url)
    export_from_ps(
        client=client,
        path_ids=ids,
        save_path=args.output,
        filter_text=args.parts_filter,
    )


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(prog='onshape')
    # Global options, shared by every subcommand (go BEFORE the subcommand)
    parser.add_argument('--env-file', '-env', type=Path, default=PROJECT_ROOT / '.env')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # onshape export --url ... --output ... [--parts-filter ...]
    export = subparsers.add_parser('export', help='Export parts from a part studio')
    export.add_argument('--url', required=True, type=str)
    export.add_argument('--output', '-o', required=True, type=Path)
    export.add_argument('--parts-filter', '-pf', default='', type=str)
    export.set_defaults(cmd_func=cmd_export)

    # Adding another subcommand is just more of the same:
    # info = subparsers.add_parser('info', help='Show document info')
    # info.add_argument('--url', required=True)
    # info.set_defaults(func=cmd_info)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    settings = OnshapeSettings(_env_file=args.env_file)
    client = OnshapeClient(settings=settings)
    args.cmd_func(client, args)


if __name__ == '__main__':
    main()
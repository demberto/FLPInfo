import argparse

from .flpinfo import FLPInfo


def main():
    arg_parser = argparse.ArgumentParser(prog="flpinfo", description=__doc__)
    arg_parser.add_argument(
        "flp",
        help="The location of FLP to show information about. Zipped FLPs are not yet supported.",
    )
    arg_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Display verbose logging output and full lists",
    )
    arg_parser.add_argument(
        "--full-lists", action="store_true", help="Lists will not appear truncated."
    )
    arg_parser.add_argument(
        "--no-color", action="store_true", help="Disables colored output"
    )
    args = arg_parser.parse_args()
    FLPInfo(args).info()


if __name__ == "__main__":
    main()

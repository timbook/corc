import os
import argparse

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-n", "--new",
        metavar="FILE",
        help="Create new corc board, maybe globally (-g)."
    )

    parser.add_argument(
        "-u", "--using",
        metavar="FILE",
        help="Which corc board to use."
    )

    parser.add_argument(
        "-g", "--global",
        dest="is_global",
        action="store_true",
        help="Determine whether to store, access, or list corc boards globally (in $HOME/.corc)."
    )

    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List possible corc boards to use."
    )

    return parser.parse_args()

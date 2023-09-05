import argparse
import logging
import os
from typing import Dict

from environ_import.util import find_dotenvs

POLL_DELAY = 0.1

_log = logging.getLogger("environ_import")


def get_files() -> Dict[str, float]:
    """Get the paths to the dotenv files that should be typed and the timestamp of when they were last modified.

    Returns
    -------
    Dict[str, float]
        A dict of paths and the timestamp of when they were last modified.
    """
    return {p: os.stat(p).st_mtime for p in find_dotenvs(True, True)}


logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser(
    prog="environ_import",
    description="Watchdog to automatically update type stubs when dotenv files are modified.",
)

parser.add_argument(
    "-o",
    "--once",
    action="store_true",
    help="run the stub generator only once and immediately exit",
)

args = parser.parse_args()

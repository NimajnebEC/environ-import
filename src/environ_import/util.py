import logging
import os
from itertools import chain
from typing import Dict, Iterable, List, Optional

from dotenv import dotenv_values, find_dotenv

from environ_import.generator import generate_stubs

__all__ = ("merge_unique", "find_dotenvs")

_log = logging.getLogger("environ_import")


def load_and_generate() -> None:
    vars = {k: v for path in find_dotenvs() for k, v in parse_dotenv(path).items()}

    # Set Environment Variables
    for k, v in vars.items():
        if k not in os.environ and v is not None:
            os.environ[k] = v

    # Generate Stubs
    generate_stubs(vars.keys())


def parse_dotenv(path: str) -> Dict[str, Optional[str]]:
    try:
        return dotenv_values(path)
    except Exception:
        _log.warn("Could not parse variables from file '%s'", path)
        return {}


def find_dotenvs() -> List[str]:
    return [find_dotenv()]


def merge_unique(*iters: Iterable[str]) -> List[str]:
    """Merges the provided iterables into a single list, ignoring duplicates.

    Parameters
    ----------
    *iters : Iterable
        The iterables to merge.

    Returns
    -------
    List[str]
        The merged list.
    """
    return list(set(chain(*iters)))

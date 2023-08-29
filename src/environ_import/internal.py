"""
Provides utilites for the package's main entrypoints.
"""

from itertools import chain
from os import environ
from typing import Iterable, List

__all__ = ["environ", "List", "initialise", "add_environ"]


def initialise() -> None:
    """Perform all module initialisation actions."""
    # None yet...


def add_environ(globals: Iterable[str]) -> List[str]:
    """Prepends all the environment variable names to the provided globals.

    Parameters
    ----------
    globals : Iterable[str]
        The global names to prepend environment variables to.

    Returns
    -------
    List[str]
        The merged list.
    """
    return merge_unique(environ.keys(), globals)


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

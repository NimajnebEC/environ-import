import importlib
import logging
import os
import re
from itertools import chain
from typing import Dict, Iterable, List, Optional

from dotenv import dotenv_values, find_dotenv

STUB_EXTENSION = ".pyi"
RE_TEMPLATE = re.compile(r"\${(.+)}")

__all__ = ("load_and_generate", "merge_unique")

_log = logging.getLogger("environ_import")


def load_and_generate() -> None:
    """Load .env files and generate module stubs for typing."""

    vars = {k: v for path in find_dotenvs() for k, v in parse_dotenv(path).items()}

    # Set Environment Variables
    for k, v in vars.items():
        if k not in os.environ and v is not None:
            os.environ[k] = v

    # Merge with .env.example for typing
    example = parse_dotenv(find_dotenv(".env.example")).keys()
    keys = merge_unique(vars.keys(), example)

    # Generate Stubs
    generate_stubs(keys)


def parse_dotenv(path: str) -> Dict[str, Optional[str]]:
    """Read and parse the dotenv file at the specifed path, ignoring any errors.

    Parameters
    ----------
    path : str
        The path to the dotenv file to parse.

    Returns
    -------
    Dict[str, Optional[str]]
        The parsed dotenv file as a dictionary.
    """

    try:
        return dotenv_values(path)
    except Exception:
        _log.warn("Could not parse variables from file '%s'", path)
        return {}


def find_dotenvs() -> List[str]:
    """Finds the paths to all dotenv files that should be loaded.

    Returns
    -------
    List[str]
        A list of paths to all dotenv files that should be loaded.
    """
    return [find_dotenv()]


def generate_stubs(keys: Iterable[str]) -> None:
    """Generate the stub files for the specified keys.

    Parameters
    ----------
    keys : Iterable[str]
        The keys to generate the stub files after.
    """
    keys = list(keys)  # fetch iterable

    write_stub(apply_template("required.txt", keys), "environ")
    write_stub(apply_template("nullable.txt", keys), "envnull")


def apply_template(file: str, keys: Iterable[str]) -> str:
    """Apply keys to the specified template file.

    Parameters
    ----------
    file : str
        The template file located in `environ_import/templates` to apply keys to.
    keys : Iterable[str]
        The keys to apply to the specifed template file.

    Returns
    -------
    str
        The result of the operation.
    """

    # Read template
    package, _ = os.path.split(__file__)
    with open(os.path.join(package, "templates", file), "r", encoding="utf-8") as f:
        template = f.read()

    # Find line and process for each key
    def repl(match: re.Match) -> str:
        line_template = match.group(1)
        return "\n".join(line_template % key for key in keys)

    result = RE_TEMPLATE.sub(repl, template, 1)
    return result


def write_stub(stub: str, module: str) -> None:
    """Write the stub for the specified module.

    Parameters
    ----------
    stub : str
        The stub to write for the module.
    module : str
        The module to write the stub for.
    """
    _log.debug("Writing stub file for module '%s'", module)

    path = importlib.import_module(module).__file__
    if path is None:
        raise ValueError(f"Could not find path of module '{module}'")

    file = os.path.splitext(path)[0] + STUB_EXTENSION
    with open(file, "w", encoding="utf-8") as f:
        f.write(stub)


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

import importlib
import logging
import os
from typing import Iterable

STUB_EXTENSION = ".pyi"

_log = logging.getLogger("environ_import")

__all__ = ("generate_stubs",)


def generate_stubs(keys: Iterable[str]) -> None:
    definition = "\n".join(f"{key}: str" for key in keys)

    write_stub(get_template() % definition, "environ")


def get_template() -> str:
    package, _ = os.path.split(__file__)
    with open(os.path.join(package, "template.txt"), "r", encoding="utf-8") as f:
        return f.read()


def write_stub(stub: str, module: str) -> None:
    _log.debug("Writing stub file for module '%s'", module)

    path = importlib.import_module(module).__file__
    if path is None:
        raise ValueError(f"Could not find path of module '{module}'")

    file = os.path.splitext(path)[0] + STUB_EXTENSION
    with open(file, "w", encoding="utf-8") as f:
        f.write(stub)

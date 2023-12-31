# Environ Import

Environ Import is a python package that allows you to import environment variables from its `environ` and `envnull` modules which are dynamically typed from `.env` files.

## Quickstart

Install using pip

```
pip install environ-import
```

Once installed, you can import environment variables from the `environ` module.

```py
from environ import PATH
print(PATH)

# or

import environ
print(environ.PATH)
```

Environ Import automatically loads `.env` files using [python-dotenv](https://github.com/theskumar/python-dotenv).

Import from the `envnull` module to avoid raising `AttributeError` when importing an undefined environment variable.

## Dynamic Typing

The [stub file](https://peps.python.org/pep-0484/#stub-files) generator is automatically run when the `environ` or `envnull` modules are imported. Types are generated based on the variables found in `.env` and `.env.example` files.

If you would like type hints to be availabe as soon a change has been made to a `.env` file, Environ Import provides a watchdog to automatically regenerate stub files when a change is detected.

```
python -m environ-import
```

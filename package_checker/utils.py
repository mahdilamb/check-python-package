"""Utility functions for the package checker."""
import contextlib
import functools
import glob
import importlib.util
import os
import re
import sys

from loguru import logger

import package_checker
from package_checker import api

PACKAGE_ROOT = os.path.normpath(
    os.path.join(
        package_checker.__file__,
        "..",
    )
)


@contextlib.contextmanager
def import_module(path: str, root=PACKAGE_ROOT):
    """Import a module from a path."""
    relative_path = os.path.relpath(path, root)
    module_path = relative_path.replace(os.path.sep, ".")[:-3]
    spec = importlib.util.spec_from_file_location(module_path, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_path] = module
    try:
        spec.loader.exec_module(module)
        yield module
    finally:
        del sys.modules[module_path]


@functools.cache
def find_tasks(
    path: str = os.path.normpath(os.path.join(__file__, "..", "tasks"))
) -> dict[str, api.Task]:
    """Find all the tasks that have been included in the framework."""
    output = {}
    for file in glob.glob(os.path.join(path, "*.py")):
        if os.path.basename(file).startswith("_"):
            continue
        with import_module(file, PACKAGE_ROOT) as module:
            try:
                output[os.path.splitext(os.path.basename(file))[0]] = next(
                    v
                    for k, v in vars(module).items()
                    if not k.startswith("_")
                    and callable(v)
                    and hasattr(v, "__task_details__")
                )

            except Exception as e:
                logger.exception(e)
    return output


def format_args(args: str) -> list[str]:
    """Format the args as a list."""
    if len(args) <= 2:
        return [args]
    if args[0] == args[-1] and args[0] in "'\"":
        return re.findall(f"{args[0]}(.*?){args[0]}", args)
    return [args]

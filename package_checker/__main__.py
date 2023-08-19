"""CLI entry point for the package checker."""
import argparse
import inspect
import json
import subprocess
import typing
from collections import defaultdict

from loguru import logger

from package_checker import api, utils

TASK_DICT = utils.find_tasks()


def split_arguments(info, groups):
    """Split the namespace by groups."""
    shared = vars(info)
    grouped: dict[str, dict[str, str]] = defaultdict(dict)
    for group, args in groups.items():
        for arg in args:
            if (val := shared.pop(arg)) not in (None, "-"):
                grouped[group][arg] = val
    return api.Github.model_validate(shared), dict(grouped)


def parser_arguments():
    """Parse arguments and return the namespace and groupings."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--github-json", type=json.dumps)
    inputs = api.Tasks(**TASK_DICT).inputs()
    groups: dict[str, list[str]] = defaultdict(list)
    for name, task in TASK_DICT.items():
        group = parser.add_argument_group(name)
        for arg, details in inputs.items():
            if (arg == "use_" + name) or arg.startswith(name):
                multiple = False
                if (
                    annotation := task.__annotations__.get(arg[len(name) + 1 :])
                ) and typing.get_origin(annotation) == typing.Annotated:
                    multiple = hasattr(
                        annotation.__args__[0], "__origin__"
                    ) and annotation.__args__[0].__origin__ in (
                        list,
                        tuple,
                        typing.Sequence,
                    )
                group.add_argument(
                    f"--{arg}",
                    help=details.get("description"),
                    default=details.get("default", "-"),
                    required=inputs["use_" + name]["required"]
                    and details.get("required", False),
                    nargs="?" if not multiple else "+",
                )
                groups[name].append(arg)

    return parser.parse_args(), dict(groups)


shared, args = split_arguments(*parser_arguments())

if shared.ref_name == shared.event.repository.default_branch:
    exit(0)
for name, task in TASK_DICT.items():
    task_args = args[name]
    if task_args.pop("use_" + name) == "false":
        continue
    task_arg_values = {k[len(name) + 1 :]: v for k, v in task_args.items()}
    task_args = inspect.getfullargspec(task).args
    shared_args = {k: v for k, v in shared.items() if k in task_args}
    all_args = {**task_arg_values, **shared_args}

    if dependencies := task.__task_details__.get("dependencies", None):
        subprocess.call(["pip", "install"] + list(dependencies))
    try:
        task(**all_args)
    except Exception as e:
        logger.exception(e)

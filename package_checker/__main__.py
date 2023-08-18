"""CLI entry point for the package checker."""
import argparse
import inspect
import subprocess
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
    return shared, dict(grouped)


def parser_arguments():
    """Parse arguments and return the namespace and groupings."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--default-branch")
    parser.add_argument("--current-branch")
    parser.add_argument("--action-yaml")
    inputs = api.Tasks(**TASK_DICT).inputs()
    groups: dict[str, list[str]] = defaultdict(list)
    for name in TASK_DICT.keys():
        group = parser.add_argument_group(name)
        for arg, details in inputs.items():
            if (arg == "use_" + name) or arg.startswith(name):
                group.add_argument(
                    f"--{arg}",
                    help=details.get("description"),
                    default=details.get("default", "-"),
                    required=inputs["use_" + name]["required"]
                    and details.get("required", False),
                )
                groups[name].append(arg)

    return parser.parse_args(), dict(groups)


shared, args = split_arguments(*parser_arguments())
actions_yaml = shared.pop("action_yaml")

if shared["current_branch"] == shared["default_branch"]:
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

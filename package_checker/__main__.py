import glob
import importlib.util
import os
import subprocess
import sys

from package_checker import _api
import yaml
import argparse


def import_module(path: str, root):
    relative_path = os.path.relpath(path, root)
    module_path = relative_path.replace(os.path.sep, ".")[:-3]
    spec = importlib.util.spec_from_file_location(module_path, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_path] = module
    spec.loader.exec_module(module)
    return module


def get_package_info():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action-yaml")
    parser.add_argument("--default-branch")
    parser.add_argument("--current-branch")
    known, unknown = parser.parse_known_args()
    with open(known.action_yaml, "rb") as fp:
        for _in, __ in yaml.safe_load(fp).get("inputs", []).items():
            parser.add_argument(
                f"--{_in}", default=__.get("default", "-"), help=__.get("description")
            )
    more = vars(parser.parse_args(unknown))
    more.update(vars(known))
    args = {k: v for k, v in more.items() if v not in {None, "-"}}
    return _api.PackageInfo(**args), os.path.normpath(
        os.path.join(known.action_yaml,  "..")
    )


package_info, PACKAGE_ROOT = get_package_info()
if package_info.current_branch == package_info.default_branch:
    exit(0)
for file in glob.glob(os.path.join(PACKAGE_ROOT, "*", "*.py")):
    if os.path.basename(file).startswith("_"):
        continue

    module = import_module(file, PACKAGE_ROOT)
    task = _api.Task(**vars(module))
    if not task.required(package_info):
        continue
    if task.dependencies:
        subprocess.call(["pip", "install"] + list(task.dependencies))
    task.run(package_info)

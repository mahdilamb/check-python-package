import glob
import importlib.util
import os
import subprocess
import sys

from package_checker import _api

PACKAGE_ROOT = os.path.normpath(os.path.join(__file__, "..", ".."))


def import_module(path: str):
    relative_path = os.path.relpath(path, PACKAGE_ROOT)
    module_path = relative_path.replace(os.path.sep, ".")[:-3]
    spec = importlib.util.spec_from_file_location(module_path, relative_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_path] = module
    spec.loader.exec_module(module)
    return module

print(os.environ["github.event.inputs.use_version_check"])

package_info = _api.PackageInfo()
for file in glob.glob(os.path.join(PACKAGE_ROOT, "*", "*.py")):
    if os.path.basename(file).startswith("_"):
        continue

    module = import_module(file)
    task = _api.Task(**vars(module))
    if not task.required(package_info):
        continue
    if task.dependencies:
        subprocess.call(["pip", "install"] + list(task.dependencies))
    task.run(package_info)

import re
import subprocess
import sys

import pkg_resources
from package_checker import _api


def required(info):
    return info.use_version_check


def run(info: _api.PackageInfo):
    subprocess.check_output(["git", "checkout", info.default_branch])
    subprocess.check_output(["git", "checkout", info.current_branch])
    version_pattern = re.compile(
        rf"^({info.version_check_variable}.*?=.*?['\"])(.*?)(['\"].*)$", flags=re.M
    )
    to_version = lambda cmd: pkg_resources.parse_version(
        version_pattern.findall(subprocess.check_output(cmd).decode())[0][1]
    )
    main = to_version(
        ["git", "show", f"{info.default_branch}:{info.version_check_path}"]
    )
    current = to_version(["cat", info.version_check_path])
    next_version = re.sub(r"^(\d+\.\d+)\.\d*(.*)$", rf"\1.{main.micro+1}\2", str(main))
    if main < current:
        with open(info.version_check_path, "r") as fp:
            text = fp.read()
            with open(info.version_check_path, "w") as fp:
                fp.write(
                    version_pattern.sub(
                        rf"\g<1>{next_version}\g<3>",
                        text,
                    )
                )

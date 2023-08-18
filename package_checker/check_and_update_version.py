import re
import subprocess
import sys

import pkg_resources

import package_checker._api


def required(info):
    return info.use_version_check
def check_version():
    path, variable, default_branch = sys.argv[1:4]

    version_pattern = re.compile(rf"^{variable}.*?=.*?[''\"](.*?)[''\"]", flags=re.M)
    to_version = lambda cmd: pkg_resources.parse_version(
        version_pattern.findall(subprocess.check_output(cmd).decode())[0]
    )
    main = to_version(["git", "show", f"{default_branch}:{path}"])
    current = to_version(["cat", path])
    assert (
        main < current
    ), f"Version of current commit ({current}) has not been incremented (from {main})."


def update_version():
    path, variable, default_branch = sys.argv[1:4]

    version_pattern = re.compile(
        rf"^({variable}.*?=.*?[''\"])(.*?)([''\"].*)$", flags=re.M
    )
    to_version = lambda cmd: pkg_resources.parse_version(
        version_pattern.findall(subprocess.check_output(cmd).decode())[0][1]
    )
    main = to_version(["git", "show", f"{default_branch}:{path}"])
    next_version = re.sub(r"^(\d+\.\d+)\.\d*(.*)$", rf"\1.{main.micro+1}\2", str(main))
    with open(path, "r") as fp:
        text = fp.read()
        with open(path, "w") as fp:
            fp.write(
                version_pattern.sub(
                    rf"\g<1>{next_version}\g<3>",
                    text,
                )
            )

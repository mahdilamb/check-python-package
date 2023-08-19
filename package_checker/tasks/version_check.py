"""Check that the version has been incremented, otherwise increment the last part."""
import re
import subprocess
from typing import Annotated

import pkg_resources

from package_checker import api


@api.task()
def main(
    github_model: api.Github,
    path: Annotated[
        str, api.Input(description="The path to the file containing the version string")
    ],
    variable: Annotated[
        str, api.Input(description="The variable name in the path provided.")
    ] = "__version__",
):
    """Run the version checker."""
    version_pattern = re.compile(
        rf"^({variable}.*?=.*?['\"])(.*?)(['\"].*)$", flags=re.M
    )
    to_version = lambda cmd: pkg_resources.parse_version(
        version_pattern.findall(subprocess.check_output(cmd).decode())[0][1]
    )
    main = to_version(
        ["git", "show", f"{github_model.event.repository.default_branch}:{path}"]
    )
    current = to_version(["cat", path])

    if main >= current:
        next_version = re.sub(
            r"^(\d+\.\d+)\.\d*(.*)$", rf"\1.{main.micro+1}\2", str(main)
        )
        with open(path, "r") as fp:
            text = fp.read()
            with open(path, "w") as fp:
                fp.write(
                    version_pattern.sub(
                        rf"\g<1>{next_version}\g<3>",
                        text,
                    )
                )

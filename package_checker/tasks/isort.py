"""isort formatter."""
from typing import Annotated

from package_checker import api, utils


@api.task(dependencies=["isort"])
def main(
    args: Annotated[
        list[str], utils.Args(description="The CLI args to be sent to isort.")
    ]
):
    """Run isort."""
    import isort.main

    isort.main.main(args)

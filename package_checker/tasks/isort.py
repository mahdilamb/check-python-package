"""Isort formatter."""
from typing import Annotated

from package_checker import api


@api.task(dependencies=["isort"])
def main(
    args: Annotated[
        list[str], api.Input(description="The CLI args to be sent to isort.")
    ]
):
    """Run isort."""
    import isort.main

    isort.main.main(args)

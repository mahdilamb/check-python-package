"""Black formatter."""
from typing import Annotated

from package_checker import api, utils


@api.task(dependencies=["black"])
def main(
    args: Annotated[
        list[str], utils.Args(description="The CLI args to be sent to black.")
    ]
):
    """Run black."""
    import black

    black.main(args)

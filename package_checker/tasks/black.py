"""Black formatter."""
from typing import Annotated

from package_checker import api


@api.task(dependencies=["black"])
def main(
    args: Annotated[str, api.Input(description="The CLI args to be sent to black.")]
):
    """Run black."""
    import black

    black.main([args])

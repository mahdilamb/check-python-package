"""Black formatter."""
from typing import Annotated

from package_checker import api, utils


@api.task(dependencies=["black"])
def main(
    args: Annotated[str, api.Input(description="The CLI args to be sent to black.")]
):
    """Run black."""
    import black

    black.main(utils.format_args(args))


(main("package_checker"))
(main("'package_checker' 'tests'"))
(main('"package_checker" "tests"'))

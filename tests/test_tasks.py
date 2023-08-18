from package_checker import utils


def find_tasks_test():
    """Check that we can find tasks."""
    assert len(utils.find_tasks())


if __name__ == "__main__":
    import sys

    import pytest

    sys.exit(pytest.main(["-v", "-s"] + sys.argv))

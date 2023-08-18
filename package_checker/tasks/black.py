"""Black formatter."""
from package_checker import api

@api.task(dependencies=["black"])
def main(args:str):
    """Run black."""
    import black
    black.main(args)

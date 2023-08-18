import dataclasses
from typing import Callable, Sequence


@dataclasses.dataclass
class PackageInfo:
    use_isort:bool = False
    use_black:bool = False
    use_version_check:bool = False


@dataclasses.dataclass(init=False)
class Task:
    dependencies: Sequence[str] | None = None
    required: Callable[[PackageInfo], bool] = lambda *_: False
    run: Callable[[PackageInfo], None] = lambda *_: None

    def __init__(self, **kwargs):
        names = set([f.name for f in dataclasses.fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)

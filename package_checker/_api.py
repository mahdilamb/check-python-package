import dataclasses
from typing import Callable, Sequence


@dataclasses.dataclass
class PackageInfo:
    action_yaml: str
    default_branch: str
    current_branch: str
    use_version_check: bool = False
    version_check_path: str | None = None
    version_check_variable: str | None = None


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

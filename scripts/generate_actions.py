"""Generate the actions.yaml file."""
import yaml

from package_checker import api, utils

INPUTS = api.Tasks(**utils.find_tasks())
DATA = {
    "name": "Check python package",
    "description": "Check a python package and commit changes for quality",
    "inputs": INPUTS.inputs(),
    "runs": {
        "using": "composite",
        "steps": [
            {"uses": "actions/setup-python@v4", "with": {"python-version": "3.10"}},
            {
                "uses": "actions/checkout@v3",
                "with": {"ref": "${{ github.event.repository.default_branch }}"},
            },
            {
                "uses": "actions/checkout@v3",
                "with": {"ref": "${{ github.ref_name }}"},
            },
            {
                "name": "Configure git",
                "run": """git config user.name github-actions && git config user.email github-actions@github.com""",
                "shell": "bash",
            },
            {
                "name": "Run package checker",
                "run": """git checkout ${{ github.event.repository.default_branch }}
git checkout ${{ github.ref_name }}
export PYTHONPATH=${{ github.action_path }}:$PYTHONPATH && pip install ${{ github.action_path }} && python -m package_checker --github-json='${{ toJSON(github) }}' """
                + f"{INPUTS.cli_args()}",
                "shell": "bash",
            },
            {
                "name": "Commit changed files",
                "run": """git status
$(git add . && git commit -m "Auto update files" && git push --set-upstream origin ${{ github.ref_name }} ) || echo "Nothing to change"
""",
                "shell": "bash",
            },
        ],
    },
}


def write_yaml(path: str, **yaml_kwargs):
    """Write the data to a yaml file."""
    with open(path, "w") as fp:
        yaml.dump(
            DATA,
            fp,
            sort_keys=False,
            line_break="\n",
            width=float("inf"),
            default_flow_style=False,
            **yaml_kwargs,
        )


if __name__ == "__main__":
    write_yaml("action.yaml")

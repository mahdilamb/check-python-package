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
            },{
                "uses": "actions/checkout@v3",
                "with": {"ref": "${{ github.ref_name }}"},
            },
            {
                "name": "Run package checker",
                "run": \
"""git checkout ${{ github.event.repository.default_branch }}
git checkout ${{ github.ref_name }}
export PYTHONPATH=${{ github.action_path }}:$PYTHONPATH && pip install ${{ github.action_path }} && python -m package_checker --default-branch=${{ github.event.repository.default_branch }} --current-branch=${{ github.ref_name }} --action-yaml=${{ github.action_path }}/action.yaml """
                + f"{INPUTS:cli_args}",
                "shell": "bash",
            },
            {
                "name": "Commit changed files",
                "run": """git status
git config user.name github-actions;
git config user.email github-actions@github.com;
$(git add . && git commit -m "Auto update files" && git push --set-upstream origin ${{ github.ref_name }} ) || echo "Nothing to change"
""",
                "shell": "bash",
            },
        ],
    },
}
with open("action.yaml", "w") as fp:
    yaml.dump(
        DATA,
        fp,
        sort_keys=False,
        line_break="\n",
        width=float("inf"),
        default_flow_style=False,
    )

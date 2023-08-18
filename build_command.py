import yaml


with open("action.yaml", "rb") as fp:
    args = " ".join(
        [
            f"--{_in}=${{{{ inputs.{_in} }}}}"
            for _in in yaml.safe_load(fp).get("inputs", [])
        ]
    )
    print(
        "export PYTHONPATH=${{ github.action_path }}:$PYTHONPATH && pip install pyyaml && python -m package_checker --default-branch=${{ github.event.repository.default_branch }} --current-branch=${{ github.ref_name }} --action-yaml=${{ github.action_path }}/action.yaml "
        + args
        + ""
    )

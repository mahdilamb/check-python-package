

import yaml


with open("action.yaml", "rb") as fp:
    args = " ".join([f"--{_in}=${{{{ inputs.{_in} }}}}" for _in in yaml.safe_load(fp).get("inputs",[])])
    print("cd ${{ github.action_path }} && pip install pyyaml && python -m package_checker --default-branch=${{ github.event.repository.default_branch }} --current-branch=${{ github.ref_name }} "+args+"")

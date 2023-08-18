

import yaml


with open("action.yaml", "rb") as fp:
    args = " ".join([f"--{_in} ${{{{ inputs.{_in} }}}}" for _in in yaml.safe_load(fp).get("inputs",[])])
    print("[ ${{ github.event.repository.default_branch }} == ${{ github.ref_name }} ] || $(cd ${{ github.action_path }} && python -m package_checker --default-branch ${{ github.event.repository.default_branch }} --current-branch ${{ github.ref_name }}"+args+")")

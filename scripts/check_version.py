import subprocess, re, pkg_resources, sys


path, variable, default_branch = sys.argv[1:4]

version_pattern = re.compile(rf"^{variable}.*?=.*?[''\"](.*?)[''\"]", flags=re.M)
to_version = lambda cmd: pkg_resources.parse_version(
    version_pattern.findall(
        subprocess.check_output(cmd).decode()
    )[0]
)
main = to_version(["git", "show", f"{default_branch}:{path}"])
current = to_version(["cat",path])
assert (
    main < current
), f"Version of current commit ({current}) has not been incremented (from {main})."

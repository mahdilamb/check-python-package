import subprocess, re, pkg_resources, sys


path, variable, default_branch = sys.argv[1:4]

version_pattern = re.compile(rf"^({variable}.*?=.*?[''\"])(.*?)([''\"].*)$", flags=re.M)
to_version = lambda cmd: pkg_resources.parse_version(
    version_pattern.findall(
        subprocess.check_output(cmd).decode()
    )[0][1]
)
main = to_version(["git", "show", f"{default_branch}:{path}"])
next_version = re.sub(r"^(\d+\.\d+)\.\d*(.*)$",fr"\1.{main.micro+1}\2", str(main))
with open(path, "r") as fp:
    text = fp.read()
    with open(path,"w") as fp:
        fp.write(version_pattern.sub(rf'\g<1>{next_version}\g<3>',text, ))
    

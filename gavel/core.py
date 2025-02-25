from subprocess import run, CalledProcessError
from shutil import rmtree
from sys import argv, exit
from pathlib import Path
from os import chmod
from stat import S_IWRITE

DIR = Path(__file__).parent
BIN = DIR / "bin"
BIN.mkdir(exist_ok=True)

def force_remove_readonly(func, path, exc_info):
    chmod(path, S_IWRITE)
    func(path)

def run_command(command: list, error_message: str):
    try:
        run(command, check=True, capture_output=True)
    except CalledProcessError:
        print(f"error: {error_message}")
        exit(1)

def parse_repo(repo: str):
    parts = repo.split('/')
    if len(parts) < 2:
        print("error: repository must be in the format 'author/repo'")
        exit(1)
    return parts[-1], '/'.join(parts[:-1])

def install(repo: str, args: list[str], use_pipx: bool = True):
    name, author = parse_repo(repo)
    dest = BIN / name

    if dest.exists():
        print(f"error: {name} is already installed.")
        exit(1)

    run_command(["git", "clone", f"https://github.com/{repo}", str(dest)], "failed to clone repository.")
    print(f"success: {name} installed to gavel bin.")

    if use_pipx:
        run_command(["pipx", "install", str(dest)], f"failed to install with pipx.\nhint: try gavel uninstall {name}, then gavel install {''.join(args)} --get-packages")
    else:
        run_command(["pip", "install", "--user", str(dest)], f"failed to install with pip.")

    print(f"success: {name} installed to system bin.")


def uninstall(name: str, args: list[str], use_pipx: bool = True):
    dest = BIN / name

    if not dest.exists():
        print(f"error: {name} is not installed.")
        exit(1)

    if args:
        pip_name_index = args.index("-n") if "-n" in args else None
        pip_name = args[pip_name_index + 1] if pip_name_index is not None and len(argv) > pip_name_index + 1 else name
    else:
        pip_name = name

    rmtree(dest, onexc=force_remove_readonly)

    print(f"success: {name} uninstalled from gavel bin.")

    if use_pipx:
        run_command(["pipx", "uninstall", pip_name], "failed to uninstall with pipx.")
    else:
        run_command(["pip", "uninstall", "-y", pip_name], "failed to uninstall with pip.")

    print(f"success: {name} uninstalled from system bin.")

def list_installed():
    packages = [d.name for d in BIN.iterdir() if d.is_dir()]
    if not packages:
        print("no installed packages.")
    else:
        print("installed packages:")
        for package in packages:
            print(f"- {package}")


def main():
    if len(argv) < 2:
        print("usage: gavel <install|uninstall|list|bin> <package> [--get-packages | -a <author>]")
        exit(1)

    command = argv[1]
    args = argv[2:]
    use_pipx = "--get-packages" not in args

    if command == "install":
        if not args:
            print("error: no repository provided.")
            exit(1)
        repo = args[0]
        author_index = args.index("-a") if "-a" in args else None
        author = args[author_index + 1] if author_index is not None and len(argv) > author_index + 1 else "fossil-org"
        trusted_authors = {
            "@dzn": "by-dazen",
            "@fsl": "fossil-org"
        }
        author = trusted_authors.get(author, author)
        install(f"{author}/{repo}", args, use_pipx)
    elif command == "uninstall":
        if not args:
            print("error: no package name provided.")
            exit(1)
        name = args[0]
        uninstall(name, args, use_pipx)
    elif command == "list":
        list_installed()
    elif command == "bin":
        print(f"local bin is located at {BIN}")
    else:
        print("error: unknown command.")
        exit(1)

if __name__ == "__main__":
    main()

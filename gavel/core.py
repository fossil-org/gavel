from subprocess import run, CalledProcessError
from shutil import rmtree
from sys import argv, exit
from pathlib import Path

DIR = Path(__file__).parent
BIN = DIR / "bin"
BIN.mkdir(exist_ok=True)


def run_command(command: list, error_message: str):
    try:
        run(command, check=True)
    except CalledProcessError:
        print(f"Error: {error_message}")
        exit(1)


def parse_repo(repo: str):
    parts = repo.split('/')
    if len(parts) < 2:
        print("Error: Repository must be in the format 'author/repo'")
        exit(1)
    return parts[-1], '/'.join(parts[:-1])


def install(repo: str, use_pipx: bool = True):
    name, author = parse_repo(repo)
    dest = BIN / name

    if dest.exists():
        print(f"Error: {name} is already installed.")
        exit(1)

    run_command(["git", "clone", f"https://github.com/{repo}", str(dest)], "Failed to clone repository.")

    if use_pipx:
        run_command(["pipx", "install", str(dest)], "Failed to install with pipx.")
    else:
        run_command(["pip", "install", "--user", str(dest)], "Failed to install with pip.")

    print(f"{name} installed successfully!")


def uninstall(name: str, args: list[str], use_pipx: bool = True):
    dest = BIN / name

    if not dest.exists():
        print(f"Error: {name} is not installed.")
        exit(1)

    if args:
        pip_name_index = args.index("-n") if "-n" in args else None
        pip_name = args[pip_name_index + 1] if pip_name_index is not None and len(argv) > pip_name_index + 1 else name
    else:
        pip_name = name

    if use_pipx:
        run_command(["pipx", "uninstall", pip_name], "Failed to uninstall with pipx.")
    else:
        run_command(["pip", "uninstall", "-y", pip_name], "Failed to uninstall with pip.")

    rmtree(dest)
    print(f"{name} uninstalled successfully!")


def update(name: str):
    dest = BIN / name
    if not dest.exists():
        print(f"Error: {name} is not installed.")
        exit(1)

    run_command(["git", "-C", str(dest), "pull"], "Failed to update repository.")
    print(f"{name} updated successfully!")


def list_installed():
    packages = [d.name for d in BIN.iterdir() if d.is_dir()]
    if not packages:
        print("No installed packages.")
    else:
        print("Installed packages:")
        for package in packages:
            print(f"- {package}")


def main():
    if len(argv) < 2:
        print("Usage: gavel <install|uninstall|update|list> <repo|package> [--get-packages]")
        exit(1)

    command = argv[1]
    args = argv[2:]
    use_pipx = "--get-packages" not in args

    if command == "install":
        if not args:
            print("Error: No repository provided.")
            exit(1)
        repo = args[0]
        author_index = args.index("-a") if "-a" in args else None
        author = args[author_index + 1] if author_index is not None and len(argv) > author_index + 1 else "fossil-org"
        trusted_authors = {
            "PXL": "pixilll",
            "FSL": "fossil-org"
        }
        author = trusted_authors.get(author, author)
        install(f"{author}/{repo}", use_pipx)
    elif command == "uninstall":
        if not args:
            print("Error: No package name provided.")
            exit(1)
        name = args[0]
        uninstall(name, args, use_pipx)
    elif command == "update":
        if not args:
            print("Error: No package name provided.")
            exit(1)
        name = args[0]
        update(name)
    elif command == "list":
        list_installed()
    else:
        print("Error: Unknown command.")
        exit(1)


if __name__ == "__main__":
    main()
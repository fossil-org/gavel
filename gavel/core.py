from subprocess import run
from shutil import rmtree
from sys import argv
from pathlib import Path

DIR = Path(__file__).parent
BIN = DIR / "bin"

def main():
    try:
        try:
            command: str = argv[1]
        except IndexError:
            print("please provide a command")
            return
        args: list = argv[2:]

        name: str = args[1] if len(args) > 1 else args[0].split('/')[-1]
        author: str = args[0] if '/' not in args[0] else '/'.join(args[0].split('/')[:-1])
        dest = BIN / name

        match command:
            case "install":
                run(["git", "clone", f"https://github.com/{args[0]}{('/'+args[1]) if len(args) > 1 else ''}", dest])
                run(["pipx", "install", dest])
            case "uninstall":
                run(["pipx", "uninstall", name])
                rmtree(dest)
    except IndexError:
        print("not enough arguments provided")
    except Exception as err:
        print(f"error: {err}")
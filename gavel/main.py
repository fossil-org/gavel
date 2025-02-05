from openway import Package, INIT
from subprocess import run
from sys import executable

def ep():
    gavel = Package("gavel", INIT)

    run([executable, gavel.get_fp("core.py")])

if __name__ == "__main__":
    ep()
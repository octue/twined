import os
import subprocess
import sys


PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


RED = '\033[0;31m'
GREEN = "\033[0;32m"
NO_COLOUR = '\033[0m'


def get_setup_version():
    process = subprocess.run(["python", "setup.py", "--version"], capture_output=True)
    return process.stdout.strip().decode("utf8")


def get_expected_semantic_version():
    process = subprocess.run(["git-mkver", "next"], capture_output=True)
    return process.stdout.strip().decode("utf8")


if __name__ == "__main__":
    os.chdir(PACKAGE_ROOT)
    setup_version = get_setup_version()
    expected_semantic_version = get_expected_semantic_version()

    if setup_version != expected_semantic_version:
        print(
            f"{RED}VERSION FAILED CHECKS:{NO_COLOUR} The version stated in 'setup.py' ({setup_version}) is different "
            f"from the expected semantic version ({expected_semantic_version})."
        )
        sys.exit(1)

    print(
        f"{GREEN}VERSION PASSED CHECKS:{NO_COLOUR} The version stated in 'setup.py' is the same as the expected "
        f"semantic version: {expected_semantic_version}."
    )
    sys.exit(0)

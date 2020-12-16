import os
import subprocess
import sys


PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class NotAVersionBranchException(Exception):
    pass


class InvalidBranchNameFormat(Exception):
    pass


def get_setup_version():
    process = subprocess.run(["python", "setup.py", "--version"], capture_output=True)
    return process.stdout.strip().decode("utf8")


def get_branch_name():
    process = subprocess.run(["git", "branch", "--show-current"], capture_output=True)
    return process.stdout.strip().decode("utf8")


def release_branch_version_matches_setup_version(setup_version, full_branch_name):
    """ Check if the package version stated in setup.py matches the semantic version 'x.y.z' included in the branch name
    of the format 'release/x.y.z'.

    :param str setup_version:
    :param str full_branch_name:
    :raise NotAVersionBranchException:
    :return bool:
    """
    try:
        branch_type, branch_name = full_branch_name.split("/")
    except ValueError:
        raise InvalidBranchNameFormat(
            f"The branch name must be in the form 'branch_type/branch_name'; received {full_branch_name!r}"
        )

    if branch_type != "release":
        raise NotAVersionBranchException(f"The branch is not a release branch: {full_branch_name!r}.")

    return branch_name == setup_version


if __name__ == "__main__":

    os.chdir(PACKAGE_ROOT)
    setup_version = get_setup_version()
    full_branch_name = get_branch_name()

    try:
        if release_branch_version_matches_setup_version(setup_version, full_branch_name):
            print(f"Release branch name matches setup.py version: {setup_version!r}.")
            sys.exit(0)

        print(
            f"Release branch name does not match setup.py version: branch is {full_branch_name!r} but setup.py version "
            f"is {setup_version!r}."
        )
        sys.exit(1)

    except NotAVersionBranchException as e:
        print(e.args[0])
        sys.exit(0)

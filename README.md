# twined

A library to help digital twins and data services talk to one another. Read more at [twined.readthedocs.io](https://twined.readthedocs.io)

[![PyPI version](https://badge.fury.io/py/twined.svg)](https://badge.fury.io/py/twined)
[![Build Status](https://github.com/octue/twined/workflows/python-ci/badge.svg)](https://github.com/octue/twined)
[![codecov](https://codecov.io/gh/octue/twined/branch/main/graph/badge.svg)](https://codecov.io/gh/octue/twined)
[![Documentation Status](https://readthedocs.org/projects/twined/badge/?version=latest)](https://twined.readthedocs.io/en/latest/?badge=latest)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Developer notes

**Documentation for use of the library is [here](https://twined.readthedocs.io). You don't need to pay attention to the following unless you plan to develop Twined itself.**

### Contributing

- Please raise an issue on the board (or add your $0.02 to an existing issue) so the maintainers know
what's happening and can advise / steer you.

- Create a fork of twined, undertake your changes on a new branch, named like *issue-84* or similar. To run tests and make commits,
you'll need to do something like:
```
git clone <your_forked_repo_address>    # fetches the repo to your local machine
cd twined                               # move into the repo directory
pyenv virtualenv 3.6.9 twinedenv        # Makes a virtual environment for you to install the dev tools into. Use any python >= 3.6
pyend activate twinedenv                # Activates the virtual environment so you don't screw up other installations
pip install -r requirements-dev.txt     # Installs the testing and code formatting utilities
pre-commit install                      # Installs the pre-commit code formatting hooks in the git repo
tox                                     # Runs the tests with coverage. NB you can also just set up pycharm or vscode to run these.
```

- Adopt a Test Driven Development approach to implementing new features or fixing bugs.

- Ask the `twined` maintainers *where* to make your pull request. We'll create a version branch, according to the
roadmap, into which you can make your PR. We'll help review the changes and improve the PR.

- Once checks have passed, test coverage of the new code is >=95%, documentation is updated and the Review is passed, we'll merge into the version branch.

- Once all the roadmapped features for that version are done, we'll release.


### Release process

The process for creating a new release is as follows:

1. Check out a branch for the next version, called `vX.Y.Z`
2. Create a Pull Request into the `main` branch.
3. Undertake your changes, committing and pushing to branch `vX.Y.Z`
4. Ensure that documentation is updated to match changes, and increment the changelog. **Pull requests which do not update documentation will be refused.**
5. Ensure that test coverage is sufficient. **Pull requests that decrease test coverage will be refused.**
6. Ensure code meets style guidelines (pre-commit scripts and flake8 tests will fail otherwise)
7. Address Review Comments on the PR
8. Ensure the version in `setup.py` is correct and matches the branch version.
9. Merge to main. Successful test, doc build, flake8 and a new version number will automatically create the release on pypi.
10. Go to code > releases and create a new release on GitHub at the same SHA.


### Building documents locally

**You don't need to do this unless you plan to develop Twined.**

Install `doxgen`. On a mac, that's `brew install doxygen`; other systems may differ.

Install sphinx and other requirements for building the docs:
```
pip install -r docs/requirements.txt
```

Run the build process:
```
sphinx-build -b html docs/source docs/build
```

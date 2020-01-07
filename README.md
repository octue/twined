# twined

A library to help digital twins talk to one another. Read more at [twined.readthedocs.io](https://twined.readthedocs.io)

[![codecov](https://codecov.io/gh/octue/twined/branch/master/graph/badge.svg)](https://codecov.io/gh/octue/twined)
[![Documentation Status](https://readthedocs.org/projects/twined/badge/?version=latest)](https://twined.readthedocs.io/en/latest/?badge=latest)
 
## Developer notes

### Contributing

- Please raise an issue on the board (or add your $0.02 to an existing issue) so the maintainers know
what's happening and can advise / steer you.

- Create a fork of twined, undertake your changes on a new branch (call it whatever you want).

- Ask the `twined` maintainers *where* to make your pull request. We'll create a version branch, according to the 
roadmap, into which you can make your PR. We'll help review the changes and improve the PR.

- Once checks have passed, test coverage of the new code is >=95%, documentation is updated and the Review is passed, we'll merge into the version branch.

- Once all the roadmapped features for that version are done, we'll release. 


### Release process

The process for creating a new release is as follows:

1. Check out a branch for the next version, called `vX.Y.Z`
2. Create a Pull Request into the `master` branch.
3. Undertake your changes, committing and pushing to branch `vX.Y.Z`
4. Ensure that documentation is updated to match changes, and increment the changelog. **Pull requests which do not update documentation will be refused.**
5. Ensure that test coverage is sufficient. **Pull requests that decrease test coverage will be refused.**
6. Ensure code meets style guidelines (flake8 tests will fail otherwise)
7. Address Review Comments on the PR
8. Ensure the version in `setup.py` is correct and matches the branch version.
9. Merge to master. Successful test, doc build, flake8 and a new version number will automatically create the release on pypi.
10. Go to code > releases and create a new release on GitHub at the same SHA.


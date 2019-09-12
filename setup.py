from setuptools import setup, find_packages

# Note:
#   The Hitchiker's guide to python provides an excellent, standard, method for creating python packages:
#       http://docs.python-guide.org/en/latest/writing/structure/
#
#   To deploy on PYPI follow the instructions at the bottom of:
#       https://packaging.python.org/tutorials/distributing-packages/#uploading-your-project-to-pypi

with open('README.md') as f:
    readme_text = f.read()

with open('LICENSE') as f:
    license_text = f.read()

setup(name='twined',
      version='0.0.1',
      py_modules=[],
      install_requires=[],
      url='https://www.github.com/octue/twined',
      license=license_text,
      author='Octue (github: octue)',
      description='A library to help digital twins talk to one another.',
      long_description=readme_text,
      packages=find_packages(exclude=('tests', 'docs'))
      )


# TODO move the following into octue example app template
# setup(
#     py_modules=['cli'],
#     install_requires=['Click'],
#     entry_points='''
#     [console_scripts]
#     octue=octue_app
#     ''',
# )

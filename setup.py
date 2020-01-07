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

setup(
    name='twined',
    version='0.0.5',
    py_modules=[],
    install_requires=['jsonschema ~= 3.2.0'],
    url='https://www.github.com/octue/twined',
    license=license_text,
    author='Octue (github: octue)',
    description='A library to help digital twins talk to one another.',
    long_description=readme_text,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=('tests', 'docs')),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6',
    keywords=['digital', 'twins', 'python', 'schema']
)

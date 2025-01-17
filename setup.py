from setuptools import setup, find_packages

# everything to make sure is done before a push (reminder for dae)
# clear the storage directory
# make a patch entry
# delete meta.json
# clear the plugins directory
# add all new commands to README.md
# UPDATE VERSION IN __init__.py
# always check if the pypi release finished successfully

def read_long_description():
    with open('README.md', encoding='utf-8') as f:
        return f.read()

setup(
    name='python3-gavel',
    version='1',
    author='dae',
    author_email='pixilreal@gmail.com',
    description='pipx that installs git repositories.',
    long_description=read_long_description(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'gavel=gavel.core:main'
        ]
    },
)

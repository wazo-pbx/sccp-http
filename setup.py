from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='sccp-http',
    version='1.3.0',
    description='HTTP interface to SCCP phone',
    # author_email='pypa-dev@googlegroups.com',  # Optional
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish
        'License :: OSI Approved :: GPLv3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='sccp softphone sccp rest',  # Optional
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    python_requires='!=2.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
    install_requires=['fastapi', 'uvicorn'],
    extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    # package_data={  # Optional
    #     'sample': ['package_data.dat'],
    # },
    # data_files=[('my_data', ['data/data_file'])],  # Optional
    entry_points={  # Optional
        'console_scripts': [
            'sample=sample:main',
        ],
    },
    project_urls={
        'Source': 'https://github.com/wazo-pbx/sccp-http',
    },
)

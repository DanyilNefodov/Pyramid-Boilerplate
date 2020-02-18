from setuptools import setup

# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
requires = [
    'alembic',
    'bcrypt',
    'deform',
    'Pillow',
    'psycopg2-binary',
    'pyramid',
    'pyramid_mako',
    'pyramid_tm',
    'sqlalchemy',
    'validators',
    'waitress',
    'zope.sqlalchemy',
]

# List of dependencies installed via `pip install -e ".[dev]"`
# by virtue of the Setuptools `extras_require` value in the Python
# dictionary below.
dev_requires = [
]

setup(
    name='server',
    install_requires=requires,
    extras_require={
        'dev': dev_requires,
    },
    entry_points={
        'paste.app_factory': [
            'main = server:main'
        ],
        'console_scripts': [
            'initialize_db = server.initialize_db:main'
        ],
    },
)

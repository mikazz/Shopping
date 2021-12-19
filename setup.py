from setuptools import setup
from shopping import __version__

setup(
    name='shopping_list_system',
    version=__version__,
    description='Shopping List System',
    package_data={"shopping_list": ["openapi/*.yaml"]},
    install_requires=[
        "connexion[swagger-ui]",
        "setuptools",
    ],
)

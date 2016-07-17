from setuptools import setup, find_packages

setup(
    name='wallme',
    version='0.5',
    packages=find_packages(),
    url='https://github.com/granitas/wallme',
    license='gpl',
    author='Bernardas Ališauskas',
    author_email='bernardas.alisauskas@gmail.com',
    description='wallme is a modular and extensible wallpaper getter and setter',
    install_requires=[
        'click',
        'requests',
        'praw',
        'parsel'
    ],
    include_package_data=True,
    entry_points="""
        [console_scripts]
        wallme=wallme.cli:cli
    """
)

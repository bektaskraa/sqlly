from setuptools import setup, find_packages

setup(
    name='SQLly',
    version='0.3',
    description='A Python library for working with SQL/noSQL databases',
    author='Bektaş Kara',
    author_email='bektaskara4@gmail.com',
    packages=['SQLly'],
    install_requires=[
        'mysql.connector',
        'psycopg2-binary',
        'colorama'
    ]
)
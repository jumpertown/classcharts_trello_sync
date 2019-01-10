from setuptools import setup


setup(
    name='classcharts_trello_sync',
    version='0.0.1',
    author='Justin Purrington',
    license='MIT',
    url='https://github.com/jumpertown/classcharts_trello_sync',
    description='Sync Classcharts data to a Trello Board.',
    install_requires=[
        'beautifulsoup4==4.7.0',
        'py-trello==0.14.0',
        'requests==2.21.0'
    ],
    packages=['classcharts_trello_sync'],
    entry_points={
        'console_scripts': [
            'classcharts_trello_sync=classcharts_trello_sync.__main__:main'
        ],
    }
)
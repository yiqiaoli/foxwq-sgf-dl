from setuptools import setup, find_packages

setup(
    name='foxwq_sgf_dl',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'sgfmill',
    ],
    entry_points={
        'console_scripts': [
            'foxwq_sgf_dl=foxwq_sgf_dl.downloader:main'  # Points to the main function in downloader.py
        ]
    }
)

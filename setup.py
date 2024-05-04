from setuptools import setup, find_packages

setup(
    name='foxwq_sgf_dl',
    version='1.0.0',
    description='A package for downloading Go game records from FoxWQ',
    author='Yiqiao Li',
    author_email='liyiqiao@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'sgfmill',
    ],
    entry_points={
        'console_scripts': [
            'foxwq_sgf_dl=foxwq_sgf_dl.downloader:main'  # Points to the main function in downloader.py
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Games/Entertainment :: Board Games',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities'
    ],
)

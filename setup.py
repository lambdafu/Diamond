#!/usr/bin/env python
# coding=utf-8

import os
from glob import glob
import platform

from setuptools import setup

if os.name == 'nt':
    pgm_files = os.environ["ProgramFiles"]
    base_files = os.path.join(pgm_files, 'diamond')
    data_files = [
        (base_files, ['LICENSE', 'README.md', 'version.txt']),
        (os.path.join(base_files, 'user_scripts'), []),
        (os.path.join(base_files, 'conf'), glob('conf/*.conf.*')),
        (os.path.join(base_files, 'collectors'), glob('conf/collectors/*')),
        (os.path.join(base_files, 'handlers'), glob('conf/handlers/*')),
    ]
    install_requires = ['ConfigObj', 'psutil', ],

else:
    data_files = [
        ('share/diamond', ['LICENSE', 'README.md', 'version.txt']),
        ('share/diamond/user_scripts', []),
    ]

    distro = platform.dist()[0]
    distro_major_version = platform.dist()[1].split('.')[0]

    data_files.append(('etc/diamond',
                       glob('conf/*.conf.*')))
    data_files.append(('etc/diamond/collectors',
                       glob('conf/collectors/*')))
    data_files.append(('etc/diamond/handlers',
                       glob('conf/handlers/*')))

    install_requires = ['ConfigObj', 'psutil', ],


def get_version():
    """
        Read the version.txt file to get the new version string
        Generate it if version.txt is not available. Generation
        is required for pip installs
    """
    try:
        f = open('version.txt')
    except IOError:
        os.system("./version.sh > version.txt")
        f = open('version.txt')
    version = ''.join(f.readlines()).rstrip()
    f.close()
    return version


def pkgPath(root, path, rpath="/"):
    """
        Package up a path recursively
    """
    global data_files
    if not os.path.exists(path):
        return
    files = []
    for spath in os.listdir(path):
        subpath = os.path.join(path, spath)
        spath = os.path.join(rpath, spath)
        if os.path.isfile(subpath):
            files.append(subpath)

    data_files.append((root + rpath, files))
    for spath in os.listdir(path):
        subpath = os.path.join(path, spath)
        spath = os.path.join(rpath, spath)
        if os.path.isdir(subpath):
            pkgPath(root, subpath, spath)

if os.name == 'nt':
    pkgPath(os.path.join(base_files, 'collectors'), 'src/collectors', '\\')
else:
    pkgPath('share/diamond/collectors', 'src/collectors')

version = get_version()

setup(
    name='diamond',
    version=version,
    url='https://github.com/BrightcoveOS/Diamond',
    author='The Diamond Team',
    author_email='https://github.com/BrightcoveOS/Diamond',
    license='MIT License',
    description='Smart data producer for graphite graphing package',
    package_dir={'': 'src'},
    packages=['diamond', 'diamond.handler'],
    data_files=data_files,
    install_requires=install_requires,
    #test_suite='test.main',
    entry_points={ 'console_scripts': [
            "diamond = diamond.main:main",
            "diamond-setup = diamond.main_setup:main" ] },
    zip_safe=False
)

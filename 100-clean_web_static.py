#!/usr/bin/python3
""" A Fabric script (based on the file `3-deploy_web_static.py`) that deletes
out-of-date archives, using the function `do_clean`
"""
from fabric.api import *


env.hosts = ['54.237.101.52', '34.229.161.29']
env.user = "ubuntu"
env.key_filename = '~/.ssh/school'


def do_clean(number=0):
    """ Cleans/deletes out-of-date archives"""

    number = int(number)

    if number == 0:
        number = 2
    else:
        number += 1

    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(path, number))

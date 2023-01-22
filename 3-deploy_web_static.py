#!/usr/bin/python3
"""A Fabric script (based on the file `2-do_deploy_web_static.py`) that creates
and distributes an archive to the web servers, using the function `deploy`
"""
from fabric.api import *
from datetime import datetime
from os import path


env.hosts = ['54.237.101.52', '34.229.161.29']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """Function to compress directory
    Return: path to archive on success; None on fail
    """

# Getting current time
    now = datetime.now()
    now = now.strftime('%Y%m%d%H%M%S')
    archive_path = 'versions/web_static_' + now + '.tgz'

    # Creating archive
    local('mkdir -p versions/')
    result = local('tar -cvzf {} web_static/'.format(archive_path))

    # Check if archiving was successful
    if result.succeeded:
        return archive_path
    return None


def do_deploy(archive_path):
    """Deploy web_static files to server
    """
    try:
        if not (path.exists(archive_path)):
            return False

        # upload archive
        put(archive_path, '/tmp/')

        # create target dir
        timestamp = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/\
releases/web_static_{}/'.format(timestamp))

        # uncompress archive and delete .tgz
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C \
/data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))

        # remove archive
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

        # move contents into host web_static
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* \
/data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))

        # remove extraneous web_static dir
        run('sudo rm -rf /data/web_static/releases/\
web_static_{}/web_static'
            .format(timestamp))

        # delete pre-existing sym link
        run('sudo rm -rf /data/web_static/current')

        # re-establish symbolic link
        run('sudo ln -s /data/web_static/releases/\
web_static_{}/ /data/web_static/current'.format(timestamp))
    except Exception as ex:
        return False

    # return True on success
    return True


def deploy():
    """Deploy web static
    """
    return do_deploy(do_pack())

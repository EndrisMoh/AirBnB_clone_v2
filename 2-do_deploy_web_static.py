#!/usr/bin/python3
"""A Fabric script (based on the file `1-pack_web_static.py`) that distributes
an archive to the web servers, using the function `do_deploy`
"""
from fabric.api import *
from datetime import datetime
from os import path


env.hosts = ['54.237.101.52', '34.229.161.29']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """Deploy web files to server
    """
    try:
        if not (path.exists(archive_path)):
            return False

            # Upload archive to the `/temp/` directory of web server
            put(archive_path, '/tmp/')

            # Create target directory on the web server
            timestamp = archive_path[-18:-4]
            run('sudo mkdir -p /data/web_static/\
releases/web_static_{}/'.format(timestamp))

            # Uncompress archive to the folder and delete .tgzr
            run('sudo tar -xzf /tmp/web_static_{}.tgz -C \
/data/web_static/releases/web_static_{}/'
                .format(timestamp, timestamp))

            # Remove archive from the web server
            run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

            # Move contents into host web_static folder
            run('sudo mv /data/web_static/releases/web_static_{}/web_static/* \
/data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))

            # Remove extraneous web_static directory
            run('sudo rm -rf /data/web_static/releases/\
web_static_{}/web_static'
                .format(timestamp))

            # Delete pre-existing symbolic link from web server
            run('sudo rm -rf /data/web_static/current')

            # Create a new symbolic link on the web server
            run('sudo ln -s /data/web_static/releases/\
web_static_{}/ /data/web_static/current'.format(timestamp))
        except Exception as ex:
            return False

        # Return True on success
        return True

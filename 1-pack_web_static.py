#!/usr/bin/python3
"""A Fabric script that generates a `.tgz` archive from the contents of the
`web_static` folder, using the function `do_pack`.
"""
from fabric.api import local
from datetime import datetime


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

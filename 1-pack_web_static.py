#!/usr/bin/python3
"""
A Fabric script that generates a .tgz archive from the contents of the 'web_static' folder
of my AirBnB Clone repo, using the function 'do_pack'
"""

from fabric.api import *
from datetime import datetime


def do_pack():
    """
    Creates an archive on web_static folder
    """
    time = datetime.now()
    archive = 'web_static_' + time.strftime("%Y%m%d%H%M%S") + '.' + 'tgz'
    local('mkdir -p versions')
    inst = local('tar -cvzf versions/{} web_static'.format(archive))
    if inst is not None:
        return archive
    else:
        return None

#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive
from the contents of the web_static folder of your AirBnB Clone repo,
using the function do_pack.
"""


def do_pack():
    """
    Fabric script that generates a .tgz archive
    """
    from fabric.api import local
    from datetime import datetime

    local("mkdir -p versions")
    created_at = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = "versions/web_static_{}.tgz".format(created_at)
    local("tar -cvzf {} web_static".format(file_path))
    return file_path


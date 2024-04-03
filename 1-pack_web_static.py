#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static folder
"""

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """Creates a .tgz archive from web_static folder"""

    # Create versions folder if it doesn't exist
    if not os.path.exists("versions"):
        local("mkdir versions")

    # Get current date and time
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")

    # Create the archive path
    archive_path = "versions/web_static_{}.tgz".format(timestamp)

    # Create the .tgz archive
    result = local("tar -czvf {} web_static".format(archive_path))

    # Check if the archive was created successfully
    if result.succeeded:
        return archive_path
    else:
        return None

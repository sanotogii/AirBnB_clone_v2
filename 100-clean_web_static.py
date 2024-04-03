#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""

from fabric.api import env, local, run
from datetime import datetime
from os import listdir
from os.path import isfile, join

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/my_ssh_private_key'  # Update with your SSH private key path

def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    try:
        number = int(number)
        if number < 0:
            return False

        # Local clean
        local_archives = local('ls -1tr versions', capture=True).split('\n')
        if number >= len(local_archives):
            return True  # No need to clean
        to_delete = local_archives[:-number]
        for archive in to_delete:
            local('rm -f versions/{}'.format(archive))

        # Remote clean
        remote_archives = run('ls -1tr /data/web_static/releases').split('\n')
        if number >= len(remote_archives):
            return True  # No need to clean
        to_delete = remote_archives[:-number]
        for archive in to_delete:
            run('rm -rf /data/web_static/releases/{}'.format(archive))

        return True
    except Exception as e:
        print(e)
        return False

# Test the do_clean function
if __name__ == "__main__":
    do_clean()

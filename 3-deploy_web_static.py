#!/usr/bin/env python3
"""
Fabric script that creates and distributes an archive to web servers
"""

from fabric.api import env, local, run
from datetime import datetime
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/my_ssh_private_key'  # Update with your SSH private key path

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "web_static_{}.tgz".format(timestamp)
        local("mkdir -p versions")
        local("tar -czvf versions/{} web_static".format(archive_name))
        return "versions/{}".format(archive_name)
    except Exception:
        return None

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Extract the archive to /data/web_static/releases/<archive filename without extension>
        filename = archive_path.split('/')[-1]
        folder_name = filename.split('.')[0]
        run('mkdir -p /data/web_static/releases/{}/'.format(folder_name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(filename, folder_name))

        # Delete the archive from the server
        run('rm /tmp/{}'.format(filename))

        # Move the contents of the archive to the appropriate folder
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'
            .format(folder_name, folder_name))

        # Remove the empty web_static folder
        run('rm -rf /data/web_static/releases/{}/web_static'.format(folder_name))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current linked to the new version
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(folder_name))

        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False

def deploy():
    """
    Deploy the latest version of the code
    """
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)

# Test the deploy function
if __name__ == "__main__":
    deploy()

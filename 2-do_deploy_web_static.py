#!/usr/bin/python3
"""
Fabric script that distributes an archive to the web servers
"""

from fabric.api import local, env, put, run
from os.path import exists
from datetime import datetime

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/my_ssh_private_key'  # Update with your SSH private key path

def do_deploy(archive_path):
    """
    Distribute an archive to the web servers
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

# Test the do_deploy function with a sample archive path
if __name__ == "__main__":
    archive_path = 'versions/web_static_{}.tgz'.format(datetime.now().strftime("%Y%m%d%H%M%S"))
    result = do_deploy(archive_path)
    if result:
        print("Deployment successful!")
    else:
        print("Deployment failed!")

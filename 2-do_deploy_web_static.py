#!/usr/bin/python3
"""
Write a Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy:
"""

from fabric.api import *
env.hosts = ['34.74.238.86', '35.196.226.115']
#env.user = "ubuntu"
#env.key_filename = "~/.ssh/holberton"


def do_deploy(archive_path):
    """ Script that does a lot of magic =) like penn and teller """
    if (archive_path is False or archive_path is None):
        return False
    try:
        # this will be the web_static_NUMBERSSSS.tgz
        last = archive_path.split("/")[-1]
        # and this will be the stuff without the dot extension
        foldName = "/data/web_static/releases/" + last.split(".")[0]
        # overwrites pre-existing remote files without request confirmation
        put(archive_path, "/tmp/")
        # make the directory on the server
        run("sudo mkdir -p {}".format(foldName))
        # unzips the archive to the folder on the webserver
        run("sudo tar -xzf /tmp/{} -C {}".format(last, foldName))
        # deletes archive from web server
        run("sudo rm /tmp/{}".format(last))
        # moves the archive out of web static to be removed
        run("sudo mv {}/web_static/* {}/".format(foldName, foldName))
        # removes the archive
        run("sudo rm -rf {}/web_static".format(foldName))
        # deletes the symbolic link to the web server
        run("sudo rm -rf /data/web_static/current")
        # create a new sym link that links to new version of code
        run("sudo ln -s {} /data/web_static/current".format(foldName))
    except:
        return False
    return True

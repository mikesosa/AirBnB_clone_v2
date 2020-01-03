#!/usr/bin/python3
"""
Write a Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy:
"""

from fabric.api import *
from datetime import datetime
from os import path


env.hosts = ['34.74.238.86', '35.196.226.115']
env.user = "ubuntu"
# env.key_filename = "~/.ssh/holberton"


def do_deploy(archive_path):
    """ Script that does a bunch of things, I havent breakfast yet :( """
    if path.isfile(archive_path) is False:
        return False
    # this will be the web_static_NUMBERSSSS.tgz
    filetgz = archive_path.split("/")[-1]
    # and this will be the stuff without the dot extension
    filename = filetgz.replace('.tgz', '')
    newdir = "/data/web_static/releases/" + filename

    try:
        # overwrites pre-existing remote files without request confirmation
        put(archive_path, "/tmp/")
        # make the directory on the server
        run("sudo mkdir {}/".format(newdir))
        # unzips the archive to the folder on the webserver
        run("sudo tar -xzf /tmp/{} -C {}/".format(filetgz, newdir))
        # deletes archive from web server
        run("sudo rm /tmp/{}".format(filetgz))
        # moves the archive out of web static to be removed
        run("sudo mv {}/web_static/* {}/".format(newdir, newdir))
        # removes the archive
        run("sudo rm -rf {}/web_static".format(newdir))
        # deletes the symbolic link to the web server
        run("sudo rm -rf /data/web_static/current")
        # create a new sym link that links to new version of code
        run("sudo ln -s {} /data/web_static/current".format(newdir))
        print("New version deployed!")
        return True
    except:
        return False

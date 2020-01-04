#!/usr/bin/python3
"""
Write a Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy:
"""

from fabric.api import *
from time import strftime
from os import path


env.hosts = ['34.74.238.86', '35.196.226.115']
env.user = "ubuntu"
# env.key_filename = "~/.ssh/holberton"


def do_pack():
    """ function that does all the the stuff above """
    time = strftime("%Y%m%d%H%M%S")
    try:
        local("sudo mkdir -p versions")
        local("sudo tar -cvzf versions/web_static_{}.tgz web_static/"
              .format(time))
    except:
        return None
    return ("versions/web_static_{}.tgz".format(time))


def do_deploy(archive_path):
    """ Script that does a bunch of things, I havent breakfast yet :( """
    if path.isfile(archive_path) is False:
        return False
    # this will be the web_static_NUMBERSSSS.tgz
    fileName = archive_path.split("/")[-1]
    # and this will be the stuff without the dot extension
    noExtension = fileName.replace('.tgz', '')
    completePath = "/data/web_static/releases/" + noExtension

    try:
        # overwrites pre-existing remote files without request confirmation
        put(archive_path, "/tmp/")
        # make the directory on the server
        run("sudo mkdir {}/".format(completePath))
        # unzips the archive to the folder on the webserver
        run("sudo tar -xzf /tmp/{} -C {}/".format(fileName, completePath))
        # deletes archive from web server
        run("sudo rm /tmp/{}".format(fileName))
        # moves the archive out of web static to be removed
        run("sudo mv {}/web_static/* {}/".format(completePath, completePath))
        # removes the archive
        run("sudo rm -rf {}/web_static".format(completePath))
        # deletes the symbolic link to the web server
        run("sudo rm -rf /data/web_static/current")
        # create a new sym link that links to new version of code
        run("sudo ln -s {} /data/web_static/current".format(completePath))
        print("New version deployed!")
        return True
    except:
        return False


def deploy():
    """ Packs and deploys. This is with no args or kwargs. """
    f = do_pack()
    return do_deploy(f) if f else False

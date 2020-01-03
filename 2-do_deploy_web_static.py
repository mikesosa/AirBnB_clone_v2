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


def do_deploy(archive_path):
    """ Deploy the file in specific folders in the servers """
    if path.isfile(archive_path) is False:
        return False
    # With .tgz
    filetgz = archive_path.split("/")[-1]
    # No .tgz
    filename = filetgz.replace('.tgz', '')

    newdir = "/data/web_static/releases/" + filename

    try:
        put(archive_path, "/tmp/")
        run("sudo mkdir {}/".format(newdir))
        run("sudo tar -xzf /tmp/{} -C {}/".format(filetgz, newdir))
        run("sudo rm /tmp/{}".format(filetgz))
        run("sudo mv {}/web_static/* {}/".format(newdir, newdir))
        run("sudo rm -rf {}/web_static".format(newdir))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(newdir))
        print("New version deployed!")
        return True
    except:
        return False

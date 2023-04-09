#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers"""

from fabric.api import env, put, run, local
from os import path

env.hosts = ["34.239.250.72", "100.26.252.126"]


def do_deploy(archive_path):
    """Distribute archive to web servers"""

    # Check if archive_path exists
    if not path.exists(archive_path):
        return False

    # Upload archive to /tmp/ directory of web server
    put(archive_path, "/tmp/")

    # Extract archive to /data/web_static/releases/<filename> on web server
    filename = archive_path.split('/')[-1]
    dirname = "/data/web_static/releases/{}".format(filename.split('.')[0])
    run("mkdir -p {}".format(dirname))
    run("tar -xzf /tmp/{} -C {}".format(filename, dirname))
    run("rm /tmp/{}".format(filename))
    run("mv {}/web_static/* {}/".format(dirname, dirname))
    run("rm -rf {}/web_static".format(dirname))

    # Delete symbolic link /data/web_static/current
    run("rm -f /data/web_static/current")

    # Create new symbolic link /data/web_static/current linked to new code
    run("ln -s {} /data/web_static/current".format(dirname))

    return True


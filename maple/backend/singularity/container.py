"""Python API for singularity interface in maple"""

import os
import random


def commit():
    """
    Commit changes from local container to local image
    """
    print("[maple.container.commit] not available for singularity backend")


def pour(options="--no-home"):
    """
    Pour local image in a container, opposite of maple rinse

    Arguments
    ---------
    options : string of options
    """
    result = os.system(
        "singularity instance start {0} \
                                                   --bind $maple_source:$maple_target \
                                                   $maple_home/images/$maple_image.sif \
                                                   $maple_container".format(
            options
        )
    )

    if result != 0:
        raise Exception("[maple] Error inside container")


def rinse(rinse_all=False):
    """
    Stop and remove the local container, opposite of maple pour

    Arguments
    ---------
    rinse_all : (True/False) flag to rinse all container
    """
    if rinse_all:
        os.system("singularity instance stop --all")
    else:
        os.system("singularity instance stop $maple_container")


def shell():
    """
    Get shell access to the local container
    """
    os.system("singularity shell --pwd $maple_target instance://$maple_container")


def run(command, options=""):
    """
    Run and rinse the local container

    Arguments
    ---------
    command : command string
    options : run options
    """
    os.environ["maple_container"] = (
        os.getenv("maple_container") + "_" + str(random.randint(1111, 9999))
    )

    command = '"{0}"'.format(command)
    result = os.system(
        "singularity exec {0} --no-home \
                                             --bind $maple_source:$maple_target \
                                             --pwd  $maple_target \
                               $maple_home/images/$maple_image.sif bash -c {1}".format(
            options, str(command)
        )
    )

    if result != 0:
        raise Exception("[maple] Error inside container")


def execute(command):
    """
    Run local image in a container

    Arguments
    ---------
    command : command string
    """
    command = '"{0}"'.format(command)
    result = os.system(
        "singularity exec --pwd $maple_target \
                                         instance://$maple_container bash -c {0}".format(
            str(command)
        )
    )

    return result


def publish(cmd_list=[]):
    """
    Publish container to an image

    Arguments
    ---------
    cmd_list: list of commands to publish
    """
    print("[maple.container.publish] not available for singularity backend")


def notebook(port="4321"):
    """
    Launch ipython notebook inside the container

    Arguments
    ---------
    port  : port id ('4321')
    """
    os.environ["maple_container"] = (
        os.getenv("maple_container") + "_" + str(random.randint(1111, 9999))
    )

    pour(options="--cleanenv")
    result = execute(
        "jupyter notebook --port={0} --no-browser --ip=0.0.0.0".format(port)
    )
    rinse()

    if result != 0:
        raise Exception("[maple] Error inside container")


def list():
    """
    List all containers on system
    """
    os.system("singularity instance list")

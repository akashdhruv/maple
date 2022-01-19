"""Python API for singularity interface in maple"""

import os

def commit(image):
    """
    Commit changes from local container to local image
    """
    print("[maple] command not available for singularity backend")

def pour(image):
    """
    Pour local image in a container, opposite of maple rinse
    """
    if(os.getenv('maple_source') and os.getenv('maple_target')):
        result = os.system('singularity instance start --containall --cleanenv \
                                                       --bind $maple_source:$maple_target \
                                                       $maple_home/{0}.sif $maple_container'.format(image))
    else:
        result = os.system('singularity instance start --containall --cleanenv \
                                                       $maple_home/{0}.sif $maple_container'.format(image))

    if result != 0: raise Exception("[maple] Error inside container")

def rinse(container='None'):
    """
    Stop and remove the local container, opposite of maple pour
    """
    if container == 'None': container = os.getenv('maple_container')
    os.system('singularity instance stop {0}'.format(container))

def shell():
    """
    Get shell access to the local container
    """
    os.system('singularity shell --pwd $maple_target instance://$maple_container')

def run(image,command):
    """
    Run and rinse the local container
    """
    pour(image)
    execute(command)
    commit(image)
    rinse()

def execute(command):
    """
    Run local image in a container
    """
    command = '"{0}"'.format(command)
    result = os.system('singularity exec --pwd $maple_target \
                                         instance://$maple_container bash -c {0}'.format(str(command)))

    if result != 0: raise Exception("[maple] Error inside container")

def notebook(port='8888'):
    """
    Launch ipython notebook inside the container
    """
    execute('jupyter notebook --port={0} --no-browser --ip=0.0.0.0'.format(port))

def list():
    """
    List all containers on system
    """
    os.system('singularity instance list')

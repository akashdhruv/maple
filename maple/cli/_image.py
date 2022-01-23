"""
Command Line Interface (CLI) for image management.
"""

import click
import os

from ..backend import Backend
from . import maple

# CLI group
#
@maple.group(name='image')
def image():
    """
    Image management, type maple image --help for more info
    """
    pass

# Build a local image using a base image 
# The modulermation supplied from Maplefile
@image.command(name='build')
@click.argument('target', required=True)
@click.argument('base', default='None')
@click.option('--as-root', is_flag=True, help='flag to build image as root')
def build(target,base,as_root):
    """
    Builds a local image from a base image
    """
    Backend().image.build(target,base,as_root)

# Pull base image from a remote registry
@maple.command(name='pull')
@click.argument('target', required=True)
@click.argument('base', required=True)
def pull(target,base):
    """
    Pull image from remote registry
    """
    Backend().image.pull(target,base)

# Push image to remote registry
# Note will require 'maple login' if credentials are required
#
@maple.command(name='push')
@click.argument('base', required=True)
@click.argument('target', required=True)
def push(base,target):
    """
    Push image to remote registry
    """
    Backend().image.push(base,target)

# Tag an image from base
@image.command(name='tag')
@click.argument('base', required=True)
@click.argument('target', required=True)
def tag(base,target):
    """
    Tag a target image from base image
    """
    Backend().image.tag(base,target)

# List all images
#
@image.command('list')
def list():
    """
    List all images on system
    """
    Backend().image.list()

# Squash and prune layers
#
@image.command('squash')
@click.argument('image', required=True)
def squash(image):
    """
    Squash and remove layers from local image, reduces size of the image
    """
    Backend().image.squash(image)

# Scan all the images
@maple.command('scan')
@click.argument('image', required=True)
def scan(image):
    """
    Scan local images, accepts multiple arguments
    """
    Backend().image.scan(image)

# Clean all local images and containers
#
@image.command('delete')
@click.argument('images', nargs=-1, required=True)
def delete(images):
    """
    Delete local images, accepts multiple arguments
    """
    for img in images:
        Backend().image.delete(img)

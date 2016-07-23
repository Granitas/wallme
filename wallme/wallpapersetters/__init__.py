import pkgutil
import importlib
import os

WALL_SETTERS = [n[1] for n in pkgutil.iter_modules([os.path.dirname(__file__)])]


def find_setter_module(name):
    return importlib.import_module('wallme.wallpapersetters.{}'.format(name))

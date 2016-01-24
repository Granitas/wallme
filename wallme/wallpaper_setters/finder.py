import pkgutil
import importlib
import os
from wallme import wallpaper_setters

WALL_SETTERS = [n for _, n, _ in pkgutil.iter_modules([os.path.dirname(wallpaper_setters.__file__)])
               if 'finder' not in n and 'base' not in n]

def get_dlmodule(name):
    return importlib.import_module('wallme.wallpaper_setters.{}'.format(name))


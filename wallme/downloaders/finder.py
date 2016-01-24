import pkgutil
import importlib
import os
from wallme import downloaders

DOWNLOADERS = [n for _, n, _ in pkgutil.iter_modules([os.path.dirname(downloaders.__file__)])
               if 'finder' not in n and 'base' not in n]

def get_dlmodule(name):
    return importlib.import_module('wallme.downloaders.{}'.format(name))



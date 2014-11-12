__author__ = 'harley'

import os
import yaml

cfg_path_abs = os.path.join(os.path.dirname(__file__), "config.yml")
# We write it in this way because it anchors the location of this .py file.
# Otherwise, directly using the relative path will be a big problem since it anchors the current working directory.
# The alternative approach will present a big problem when we run or import the this python script from an outside directory
with open(cfg_path_abs, 'r') as ymlfile:
    clicfg = yaml.load(ymlfile)


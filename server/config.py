__author__ = 'main'

import os, sys
import yaml


from sqlalchemy.engine.url import URL as AlchemyURL

# from server.mysqlDB import MysqlDB
cfg_path_abs = os.path.join(os.path.dirname(__file__), "config.yml")
# We write it in this way because it anchors the location of this .py file.
# Otherwise, directly using the relative path will be a big problem since it anchors the current working directory.
# The alternative approach will present a big problem when we run or import the this python script from an outside directory
with open(cfg_path_abs, 'r') as ymlfile:
    svrcfg = yaml.load(ymlfile)

svrcfg['SQLALCHEMY_DATABASE_URI'] = AlchemyURL(**svrcfg['db'])
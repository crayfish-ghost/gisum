import os
from configparser import ConfigParser
BASE_DIR = os.path.abspath( os.path.dirname(__file__) )
config = ConfigParser()
config.read(BASE_DIR + "/../config.ini", encoding='utf-8')

import os
from configparser import ConfigParser


class Configuration:
    def __init__(self, environment=os.environ.get('ASK_ENV', 'development')):
        self.config = ConfigParser()
        self.config.read('../conf/environments/%s.ini' % environment)

    def config_get(self, section, option):
        return self.config.get(section, option)

    def use_custom_config_file(self, file):
        self.config = ConfigParser()
        self.config.read(file)

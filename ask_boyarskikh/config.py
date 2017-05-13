from configparser import ConfigParser, NoSectionError, NoOptionError

class Configuration:
	def __init__(self):
		self.config = ConfigParser()
		self.config.read("../conf/config.ini")

	def config_get(self, section, option, default=None):
		return self.config.get(section, option)

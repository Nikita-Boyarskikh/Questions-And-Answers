from configparser import ConfigParser, NoSectionError, NoOptionError

class Configuration:
	def config_get(self, section, option, default=None):
		self.config = ConfigParser()
		self.config.read("../conf/config.ini")
		return self.config.get(section, option)

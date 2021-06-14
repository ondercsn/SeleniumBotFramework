from user_agent import generate_user_agent

class UserAgent():

	def __init__(self, db, logger):
		self.db = db
		self.logger = logger

	def generate(self, os='win', navigator="chrome"):
		useragentString = generate_user_agent(os=os, navigator=navigator)
		return self.set(useragentString=useragentString,browserType=navigator)

	def from_string(self,useragent_str, browser_type='chrome'):
		self._useragent = self.set(useragentString=useragent_str, browserType=browser_type)
		return self._useragent


	def set(self, useragentString=None, browserType=None, screenSize=None):
		self.browser_type = browserType
		self.agent_string = useragentString
		self.screen_size = screenSize

		return self

	def __repr__(self):
		return {
			"agent_string": self.agent_string,
			"browser_type": self.browser_type,
			"screen_size": self.screen_size
		}

	def __str__(self):
		return str(self.__repr__())

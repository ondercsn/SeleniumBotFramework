import zipfile, os

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.firefox.options import Options

from bot.lib.functions import *


class Browser:

	def __init__(self, logger, browserPath, useragent=None, proxy=None, headless=False):
		self.logger = logger
		self.browser = None
		self.browserID = 0
		self.PID = None

		self.browserPath = browserPath
		self.useragent = useragent
		self.proxy=proxy
		self.headless = headless

		self.page_load_strategy = None #"eager"
		self.browser_size = None

	def set_proxy(self, options):
		if self.proxy is not None:
			manifest_json = """
			{
				"version": "1.0.0","manifest_version": 2,"name": "Chrome Proxy",
				"permissions": ["proxy","tabs","unlimitedStorage","storage","<all_urls>","webRequest","webRequestBlocking"],
				"background": {"scripts": ["background.js"]},"minimum_chrome_version":"22.0.0"
			}
			"""
			background_js = """
			var config = {mode: "fixed_servers",rules: {singleProxy: {scheme: "http",host: "%s",port: parseInt(%s)},bypassList: ["localhost"]}};
			chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
			function callbackFn(details) {return {authCredentials: {username: "%s",password: "%s"}};}
			chrome.webRequest.onAuthRequired.addListener(callbackFn,{urls: ["<all_urls>"]},['blocking']);
			""" % (self.proxy.address, self.proxy.port, self.proxy.username, self.proxy.password)

			userEntry = ""
			if self.proxy.username is not None:
				userEntry = self.proxy.username + ":" + self.proxy.password + "@"

			protocol = "http://" if self.proxy.protocol is None else "%s://" % self.proxy.protocol
			_proxy = protocol + userEntry + self.proxy.address + ":" + self.proxy.port
			options.add_argument("--proxy-server=%s" % _proxy)

			pluginfile = os.path.join('', 'drivers', 'chrome_extension', 'proxy_auth_plugin.zip')

			with zipfile.ZipFile(pluginfile, 'w') as zp:
				zp.writestr("manifest.json", manifest_json)
				zp.writestr("background.js", background_js)

			return pluginfile
		else:
			self.logger.info("No proxy defined")
			return None


	def hide_selenium_extension(self, create=True):
		ext_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "drivers", "chrome_extension")
		org_zip_file = os.path.join(ext_path, "hs_extension.xpi")

		if create:
			files = ["manifest.json", "content.js", "arrive.js"]
			with zipfile.ZipFile(org_zip_file, "w", zipfile.ZIP_DEFLATED, False) as zipf:
				for file in files:
					zipf.write(os.path.join(ext_path, file), file)

		new_zip_file = os.path.join(ext_path, "tmp", "hs_extension_" + str(self.browserID) + ".xpi")
		open(new_zip_file, 'wb').write(open(org_zip_file, 'rb').read())

		return new_zip_file


	def delete_extensions(self):
		hsfile = os.path.join("", "drivers", "chrome_extension", "hs_extension_" + self.browserID + ".xpi")
		os.remove(hsfile)


	def create_browser(self, browser_type=None):
		self.browserID = random.randint(1,999999)

		if not browser_type:
			if self.useragent and self.useragent.browser_type == "chrome" :
				browser = self.Chrome()
			else:
				browser = self.Firefox()

		else:
			if browser_type == "chrome":
				browser = self.Chrome()
			else:
				browser = self.Firefox()

		self.PID = browser.service.process.pid
		self.browser = browser

		return browser


	def Chrome(self):
		browser = None

		options = chrome_options()

		if self.headless:
			options.add_argument('--headless')

		caps = DesiredCapabilities.CHROME
		caps["resolution"] = "1024x768"

		caps["marionette"] = True
		caps["ensureCleanSession"] = True
		caps["chrome.switches"] = ["disk-cache-size=0", "network.http.use-cache=0"]
		caps["pageLoadStrategy"] = "none"
		
		proxyExtension = self.set_proxy(options)

		if proxyExtension is not None:
			options.add_extension(proxyExtension)

		options.add_extension(self.hide_selenium_extension(create=True))

		prefs = {"profile.default_content_setting_values.notifications": 2}
		options.add_experimental_option("prefs", prefs)

		screen = None
		ua = None

		if self.useragent:
			if self.useragent.agent_string:
				ua = self.useragent.agent_string
				options.add_argument("user-agent=%s" % ua)

			if self.useragent.screen_size:
				screen = self.useragent.screen_size
				nScreen = screen.split('x')
				options.add_argument("window-size=%s,%s" % (nScreen[0],nScreen[1]))

		try:
			browser = webdriver.Chrome(executable_path=self.browserPath, options=options, desired_capabilities=caps)
			browser.delete_all_cookies()
			
			if screen is not None:
				try:
					nScreen = screen.split('x')
					browser.set_window_size(nScreen[0],nScreen[1])
				except Exception as e:
					raise Exception('screen size couldnt be adjusted',e)

			return browser

		except Exception as e:
			self.logger.error("Error creating browser : ",str(e))
			raise Exception("Error creating browser : ",e)


	def Firefox(self):
		browser = None
		options = Options()
	
		if self.headless:
			options.headless = True

		options.add_argument('--disable-gpu')

		profile = webdriver.FirefoxProfile()

		profile.set_preference("network.http.use-cache", True)
		profile.set_preference("browser.cache.offline.enable", True)
		profile.set_preference("browser.cache.disk.enable", True)
		profile.set_preference("browser.cache.memory.enable", True)

		'''
		profile.set_preference("network.http.use-cache", False)
		profile.set_preference("browser.cache.offline.enable", False)
		profile.set_preference("browser.cache.disk.enable", False)
		profile.set_preference("browser.cache.memory.enable", False)
		
		profile.set_preference("browser.sessionhistory.max_entries", "10")
		profile.set_preference("browser.display.show_image_placeholders;true", False)
		profile.set_preference("image.mem.animated.discardable", False)
		'''
	
		ffox_cap = DesiredCapabilities.FIREFOX
		ffox_cap["screen-resolution"] = "1280x1024x24"
		ffox_cap['marionette'] = True
		#ffox_cap["binary"] = "C:\\Program Files\\Firefox Developer Edition\\firefox.exe"
		ffox_cap['ensureCleanSession'] = True
		ffox_cap['pageLoadStrategy'] = self.page_load_strategy

		if self.proxy.address:
			profile.set_preference('network.proxy.type', 1)

			_proxyuser = ""
			if self.proxy.username and self.proxy.password:
				_proxyuser = "%s:%s@" % (self.proxy.username,self.proxy.password)

			_proxy = "%s%s:%s" % (_proxyuser,self.proxy.address,self.proxy.port)

			ffox_cap['proxy'] = {"proxyType": "MANUAL","httpProxy": _proxy,"sslProxy": _proxy}

		ua = self.useragent.agent_string
		screen = self.useragent.screen_size if self.useragent.screen_size is not None else "1024x768"

		profile.set_preference("general.useragent.override", ua)
		profile.DEFAULT_PREFERENCES['frozen']['xpinstall.signatures.required'] = False

		try:
			browser = webdriver.Firefox(executable_path=self.browserPath, capabilities=ffox_cap,
										firefox_profile=profile, options=options, service_log_path=os.path.devnull)

		except Exception as e:
			print(e)

		browser.delete_all_cookies()

		profile.set_preference('xpinstall.signatures.required', 'false')
		browser.install_addon(self.hide_selenium_extension(), temporary=True)

		try:
			nScreen = screen.split('x')
			browser.set_window_size(nScreen[0],nScreen[1])
		except:
			pass

		return browser


	def close(self, kill=True):
		#self.delete_extensions()
		#log('closing process')
		self.browser.close()
		self.browser.quit()

		"""
		if kill:
			try:
				p = psutil.Process(self.PID)
				p.terminate()
				print("Kill process : ",self.PID)
			except:
				pass
		"""
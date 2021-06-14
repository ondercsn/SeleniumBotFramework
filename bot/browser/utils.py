import os
import pickle
import random
import sys

import psutil
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from bot.lib.time_util import sleep


def explicit_wait(browser, track, ec_params, timeout=35, notify=True):
	"""
	Explicitly wait until expected condition validates

	:param browser: webdriver instance
	:param track: short name of the expected condition
	:param ec_params: expected condition specific parameters - [param1, param2]
	"""

	# list of available tracks:
	# <https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/
	# selenium.webdriver.support.expected_conditions.html>

	if not isinstance(ec_params, list):
		ec_params = [ec_params]

	# find condition according to the tracks
	if track == "VOEL":
		elem_address, find_method = ec_params
		ec_name = "visibility of element located"

		find_by = (
			By.XPATH if find_method == "XPath"
			else By.CSS_SELECTOR
			if find_method == "CSS"
			else By.CLASS_NAME
		)
		locator = (find_by, elem_address)
		condition = ec.visibility_of_element_located(locator)

	elif track == "TC":
		expect_in_title = ec_params[0]
		ec_name = "title contains '{}' string".format(expect_in_title)

		condition = ec.title_contains(expect_in_title)

	elif track == "PFL":
		ec_name = "page fully loaded"
		condition = lambda browser: browser.execute_script(
			"return document.readyState"
		) in ["complete" or "loaded"]

	elif track == "SO":
		ec_name = "staleness of"
		element = ec_params[0]

		condition = ec.staleness_of(element)

	try:
		if timeout == None:
			timeout=35
		wait = WebDriverWait(browser, timeout)
		result = wait.until(condition)

	except TimeoutException:
		#print ("Timed out with failure while explicitly waiting until {}!\n".format(ec_name))
		result = None
		#raise Exception ("Timed out with failure while explicitly waiting until {}!\n".format(ec_name))

	return result


def load_session(browser, username, cookie_path):
	path = os.path.join(cookie_path, browser.capabilities['browserName'], username)
	if (os.path.exists(path)):
		with open(path, 'rb') as cookiesfile:
			try:
				cookies = pickle.load(cookiesfile)
				for cookie in cookies:
					browser.add_cookie(cookie)
				return True
			except:
				return False
	else:
		return False

def save_session(browser, username, cookie_path):
	dirpath = os.path.join(cookie_path, browser.capabilities['browserName'])

	if not os.path.exists(dirpath):
		os.makedirs(dirpath)

	filePath = os.path.join(dirpath, username)

	with open(filePath, 'wb') as filehandler:
		pickle.dump(browser.get_cookies(), filehandler)
		return True

def get_current_url(browser):
	try:
		current_url = browser.execute_script("return window.location.href")

	except WebDriverException:
		try:
			current_url = browser.current_url
		except WebDriverException:
			current_url = None

	return current_url


def web_address_navigator(browser, link, delay_after_call=2):
	current_url = get_current_url(browser)
	page_type = None  # file or directory

	if current_url is not None and current_url.endswith("/"):
		current_url = current_url[:-1]

	if link.endswith("/"):
		link = link[:-1]
		page_type = "dir"  # slash at the end is a directory

	new_navigation = current_url != link

	if current_url is None or new_navigation:
		link = link + "/" if page_type == "dir" else link  # directory links

		try:
			browser.get(link)
			return True
		except:
			return False


def take_rotative_screenshot(browser, logfolder):
	global next_screenshot

	if next_screenshot == 1:
		browser.save_screenshot("{}screenshot_1.png".format(logfolder))
	elif next_screenshot == 2:
		browser.save_screenshot("{}screenshot_2.png".format(logfolder))
	else:
		browser.save_screenshot("{}screenshot_3.png".format(logfolder))
		next_screenshot = 0

	next_screenshot += 1


def scroll_bottom(browser, element, range_int):
	if range_int > 50:
		range_int = 50

	for _ in range(int(range_int / 2)):
		browser.execute_script("window.scrollBy(0, 1000)")
		sleep(1)

	return


def scroll_to_most_bottom(browser):
	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	sleep(1)
	return


def click_element(browser, element, keys=None, click=1, delay_between_clicks=True):

	try:
		browser.execute_script("arguments[0].scrollIntoView()", element)
		sleep(0.5)

		actionP = ActionChains(browser).move_to_element(element)
		if click == 1:
			actionP.click().perform()
		elif click == 2:
			actionP.double_click().perform()

		if keys :
			for char in keys:
				element.send_keys(char)
				if delay_between_clicks:
					sleep(random.uniform(0.1, 0.4))
		return True

	except Exception as e:
		return False


def get_page_title(browser):
	explicit_wait(browser, "PFL", [], 10)

	try:
		page_title = browser.title
	except WebDriverException:
		try:
			page_title = browser.execute_script("return document.title")
		except WebDriverException:
			try:
				page_title = browser.execute_script("return document.getElementsByTagName('title')[0].text")
			except WebDriverException:
				return None

	return page_title


def reload_webpage(browser, delay=2):
	browser.execute_script("location.reload()")
	sleep(delay)
	return True


def click_visibly(browser, element):
	if element.is_displayed():
		click_element(browser, element)

	else:
		browser.execute_script(
			"arguments[0].style.visibility = 'visible'; "
			"arguments[0].style.height = '10px'; "
			"arguments[0].style.width = '10px'; "
			"arguments[0].style.opacity = 1",
			element,
		)
		click_element(browser, element)

	return True


def extract_text_from_element(elem):
	if elem and hasattr(elem, "text") and elem.text:
		text = elem.text
	else:
		text = None

	return text



def kill():
	os.popen("pgrep -f %s | xargs kill" % "firefox")
	os.popen("pgrep -f %s | xargs kill" % "chrome")
	os.popen("pgrep -f %s | xargs kill" % "geckodriver")
	os.popen("pgrep -f %s | xargs kill" % "chromedriver")


def kill_all_browser_processes():
	try:
		tr1= os.popen("taskkill /IM firefox.exe /F")
		tr2 = os.popen("taskkill /IM geckodriver.exe /F")
	except:
		pass


def kill_process(pid):
	try:
		p = psutil.Process(pid).terminate()
	except:
		print('Couldnt kill process', sys.exc_info())

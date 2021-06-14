import datetime
import inspect

from bot.browser.browser import Browser
from bot.models.profile import Profile
from bot.models.proxy import Proxy
from bot.models.email import Email
from bot.models.useragent import UserAgent


class Bot:

    def __init__(self, db_object, logger=None):
        self.db_object = db_object
        self.logger = logger

        self.proxy = Proxy(db_object, logger)
        self.email = Email(db_object, logger)
        self.useragent = UserAgent(db_object, logger)
        self.profile = Profile(db_object, logger)


    def create_browser(self, browserPath, browser_type, headless=False):
        browser = Browser(logger=self.logger,
                          browserPath=browserPath,
                          proxy=self.proxy,
                          useragent=self.useragent,
                          headless=headless
                          )
        browser.create_browser(browser_type)



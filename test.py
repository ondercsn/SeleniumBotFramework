import logging
import time

from bot.bot import Bot
from bot.db._sqlite import DB

from bot.browser.browser import Browser

#db=DB("127.0.0.1","root","1234","botbase")
db = DB("bot/db/db.db")

logger = logging.getLogger('botloger')
hdlr = logging.FileHandler('bot.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


bot = Bot(db,logger)
bot.create_browser(
    browserPath="bot/browser/drivers/win/chromedriver.exe",
    browser_type="chrome",
    headless=False
)






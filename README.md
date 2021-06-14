# SeleniumBotFramework
A general purpose bot framework uses selenium. It has ready to use proxy,email,profile, useragent implementations  

Sample usage : 

```
import logging
import time

from bot.bot import Bot
from bot.db._sqlite import DB
from bot.browser.browser import Browser

db = DB("db.db")

logger = logging.getLogger('botloger')
hdlr = logging.FileHandler('bot.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)


bot = Bot(db,logger)
bot.create_browser(
    browserPath="bot/browser/drivers/win/chromedriver.exe",
    browser_type="chrome",
    headless=False
)
time.sleep(1000)
```





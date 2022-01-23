import random
import asyncio
from configparser import ConfigParser
from vkbottle import load_blueprints_from_package
from vkbottle.bot import Bot
import asyncio
from vkbottle.api import API
import sys
from orm import init
from vkbottle import CtxStorage
from vkbottle import LoopWrapper
from vkbottle.user import rules

lw = LoopWrapper()
config = ConfigParser()
config.read("config.ini")

bot = Bot(token=config.get("bot", "token"))
bot.loop_wrapper = lw


if __name__ == '__main__':
    storage = CtxStorage()

    for i in load_blueprints_from_package('blueprints'):
        i.load(bot)

    loopW = asyncio.get_event_loop()

    lw.add_task(bot.run_polling())
    lw.add_task(init())

    bot.run_forever()

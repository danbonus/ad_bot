import logging
import sys
from configparser import ConfigParser

from vkbottle import load_blueprints_from_package
from vkbottle.api import API
from vkbottle.bot import Bot

from announce import announce
from models.announcer import Announcer
from orm import init
from utils.UtilsMiddleware import UtilsMiddleware
from utils.loop_wrapper.loop_wrapper import LoopWrapper
from utils.storage import CtxStorage

logger = logging.getLogger("vkbottle")
logger.setLevel(20)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    u'[%(asctime)s] %(levelname)s: %(message)s ' + '(%(filename)s:%(threadName)s:%(funcName)s:%(lineno)s)',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


lw = LoopWrapper()
config = ConfigParser()
config.read("config.ini")

bot = Bot(token=config.get("bot", "token"))
bot.loop_wrapper = lw


async def init_and_generate():
    await init()
    await generate_api()


async def generate_api():
    storage['announcers'] = {user.uid: API(user.token) for user in await Announcer.all()}


if __name__ == '__main__':
    storage = CtxStorage()

    blueprints = []
    end_blueprints = {"Menu": None}
    for i in load_blueprints_from_package('blueprints'):
        if i.name in end_blueprints.keys():
            end_blueprints[i.name] = i
        else:
            blueprints.append(i)

    for i in blueprints:
        i.load(bot)

    for i, _ in end_blueprints.items():
        _.load(bot)


    lw.add_task(init_and_generate())
    lw.create_interval(announce, minutes=1, storage=storage)
    bot.labeler.message_view.register_middleware(UtilsMiddleware)
    bot.run_forever()

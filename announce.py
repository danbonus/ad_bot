from datetime import datetime

from vkbottle import API

from models.announcement import Announcement
from models.group import Group
from utils.storage import CtxStorage
from utils.utils import send_ad


async def announce(storage: CtxStorage):
    debug = False
    print('looking for announces')
    for i in await Announcement.all():
        print(i.name)
        api: API = storage['announcers'][i.announcer_uid]
        for time in i.time:
            print(time)
            print(i.time)
            time = time.split(":")
            hour = int(time[0])
            minute = int(time[1])

            print(hour)
            print(minute)
            if hour == datetime.now().hour and minute == datetime.now().minute or debug:
                await send_ad(api, i, await Group.all())

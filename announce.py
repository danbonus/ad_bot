from models.announcement import Announcement
from models.group import Group
from datetime import datetime
from utils.storage import CtxStorage
from vkbottle import API
import json


message = f"""
⚠ Обмена нет.
Даже не спрашивайте.

💸 Цена: %sр, до вас доеду за 150р.

%s

Ⓜ Купчино / Шушары 
"""


async def announce(storage: CtxStorage):
    print('looking for announces')
    for i in await Announcement.all():
        print(i.name)
        api: API = storage['announcers'][i.announcer_uid]
        for time in json.loads(i.time):
            time = time.split(":")
            hour = int(time[0])
            minute = int(time[1])

            print(hour)
            print(minute)
            if hour == datetime.now().hour and minute == datetime.now().minute:
                for group in await Group.all():
                    print(group.uid)
                    print(i.attachments)

                    await api.wall.post(
                        owner_id=group.uid,
                        message=message % (str(i.price), i.text),
                        attachments=json.loads(i.attachments)
                    )

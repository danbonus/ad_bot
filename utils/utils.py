from datetime import datetime

from utils.storage import CtxStorage

message = f"""
⚠ Обмена нет.
Даже не спрашивайте.

💸 Цена: %sр, до вас доеду за 150р.

%s

Ⓜ Купчино / Шушары 
"""


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


async def send_ad(api, announcement, groups):
    storage = CtxStorage()
    print("Sending!")
    for group in groups:
        time = datetime.now().strftime("%d.%m.%Y | %H:%M:%S")
        try:
            await api.wall.post(
                owner_id=group.uid,
                message=message % (str(announcement.price), announcement.text),
                attachments=announcement.attachments
            )
            log = {"ad_name": announcement.name, "group": f"vk.com/club{abs(group.uid)}", 'time': time}
        except Exception as e:
            log = {"ad_name": "ERROR", "group": e, "time": time}

        if 'log' in storage:
            storage['log'].append(log)
        else:
            storage['log'] = [log]

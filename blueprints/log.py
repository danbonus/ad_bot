from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from utils.keyboard import BACK_TO_MENU

bp = Blueprint()
bp.name = "Log"


@bp.on.private_message(payload={"cmd": "view_log"})
async def view_log(message: Message, no_section_storage):
    if 'log' in no_section_storage:
        text = "Последние 10 записей: \n\n"
        log = no_section_storage['log']
        incr = 0
        print(log)
        for i in log[::-1]:
            incr += 1
            if incr == 11:
                break
            print(i)
            text += f"Объявление {i['ad_name']} выложено в группе {i['group']} в {i['time']}\n"
        await message.answer(text, keyboard=BACK_TO_MENU)
    else:
        await message.answer("Не разослано", keyboard=BACK_TO_MENU)

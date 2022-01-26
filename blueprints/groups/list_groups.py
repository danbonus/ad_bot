from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from models.group import Group
from utils.keyboard import get_groups, BACK_TO_MENU

bp = Blueprint()
bp.name = "List announcements"


@bp.on.message(text="Посмотреть группы")
@bp.on.message(payload={"cmd": "show_groups"})
async def show_groups(message: Message, no_section_storage):
    api = no_section_storage['announcers'][message.from_id]
    msg, keyboard = await get_groups(api, await Group.all())
    await message.answer(msg, keyboard=BACK_TO_MENU)


from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from models.announcement import Announcement
from utils.keyboard import get_announcements_to_show, BACK_TO_MENU
from utils.states import UtilsStates

bp = Blueprint()
bp.name = "List announcements"


@bp.on.message(text="Посмотреть объявления")
@bp.on.message(payload={"cmd": "show_announcements"})
async def show_announcements(message: Message):
    msg, keyboard = get_announcements_to_show(await Announcement.all())
    await message.answer(msg, keyboard=keyboard + BACK_TO_MENU)
    await bp.state_dispenser.set(message.peer_id, UtilsStates.SEND_STATE)

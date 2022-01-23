import json
from models.announcement import Announcement

from datetime import datetime
from vkbottle.bot import Message
from vkbottle import Keyboard, Text

from vkbottle.bot import Blueprint

from utils.keyboard import MENU_KEYBOARD, BACK_TO_MENU
from utils.states import AnnouncementCreationStates
from vkbottle import CtxStorage

bp = Blueprint()
bp.name = "Create announcement"


@bp.on.message(text="Создать объявление")
@bp.on.message(payload={"cmd": "create_announcement"})
async def create_announcement(message: Message):
    await bp.state_dispenser.set(message.peer_id, AnnouncementCreationStates.GET_NAME)
    await message.answer("Введи название объявления.", keyboard=BACK_TO_MENU)


@bp.on.message(state=AnnouncementCreationStates.GET_NAME)
async def get_name(message: Message):
    CtxStorage().set(f"{message.from_id}_name", message.text)
    await bp.state_dispenser.set(message.peer_id, AnnouncementCreationStates.GET_TEXT)
    return "Ок, название получил. Ты спецом такое уебское придумал? Кринж.. бляяя. Вводи текст объявы"


@bp.on.message(state=AnnouncementCreationStates.GET_TEXT)
async def get_description(message: Message):
    await bp.state_dispenser.set(message.peer_id, AnnouncementCreationStates.GET_ATTACHMENTS)

    CtxStorage().set(f"{message.from_id}_status_desc", message.text)
    return "Ага, теперь и эту хуйню записал. Пиздец, чем я занимаюсь на старость лет? " \
           "Присылай картинки к объяве."


@bp.on.message(state=AnnouncementCreationStates.GET_ATTACHMENTS)
async def get_text(message: Message):
    await bp.state_dispenser.set(message.peer_id, AnnouncementCreationStates.GET_PRICE)

    CtxStorage().set(f"{message.from_id}_status_desc", message.text)
    return "Присылай цену."


@bp.on.message(state=AnnouncementCreationStates.GET_PRICE)
async def get_description(message: Message):
    await bp.state_dispenser.set(message.peer_id, AnnouncementCreationStates.GET_TIME)

    CtxStorage().set(f"{message.from_id}_status_desc", message.text)
    return "В какое время рассылать? Пример: 16:00, 20:00. Да, можно через запятую"


@bp.on.message(state=AnnouncementCreationStates.GET_TIME)
async def get_description(message: Message):
    announcement = await Announcement.create(
        name=CtxStorage().get(f"{message.from_id}_status_name"),
        description=CtxStorage().get(f"{message.from_id}_status_desc"),
        text=message.text
    )
    await bp.state_dispenser.delete(message.peer_id)
    return "Ну всё, блять, молодец. Создано."

import json

from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from models.announcement import Announcement
from utils.keyboard import BACK_TO_MENU, get_announcements_to_delete, CONFIRMATION_KEYBOARD
from utils.states import AnnouncementDeletionStates

bp = Blueprint()
bp.name = "Delete announcement"


@bp.on.message(text="Удалить объявление")
@bp.on.message(payload={"cmd": "delete_announcement"})
async def delete_announcement(message: Message):
    keyboard = get_announcements_to_delete(await Announcement.all(), 3)
    await message.answer("Выбери объяву.", keyboard=keyboard)
    await bp.state_dispenser.set(message.peer_id, AnnouncementDeletionStates.GET_ID)


@bp.on.message(state=AnnouncementDeletionStates.GET_ID)
async def get_id(message: Message, storage):
    storage['ad_id'] = json.loads(message.payload)['id']
    await bp.state_dispenser.set(
        message.peer_id,
        AnnouncementDeletionStates.CONFIRMATION_STATE,
    )
    await message.answer("Дa/нет?", keyboard=CONFIRMATION_KEYBOARD)


@bp.on.message(state=AnnouncementDeletionStates.CONFIRMATION_STATE)
async def confirm(message: Message, storage):
    uid = json.loads(message.payload)
    if uid['status']:
        announcement = await Announcement.get(id=storage['ad_id'])
        await announcement.delete()
        await message.answer("ок, удалено.", keyboard=BACK_TO_MENU)
    else:
        await message.answer("ну и иди нахуй.", keyboard=BACK_TO_MENU)

    await bp.state_dispenser.delete(message.peer_id)

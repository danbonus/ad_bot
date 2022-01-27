import json

from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from models.announcement import Announcement
from utils.keyboard import BACK_TO_MENU, get_announcements, CONFIRMATION_KEYBOARD, ANNOUNCEMENT_EDITING_KEYBOARD
from utils.states import AnnouncementEditingStates
from utils.utils import message as msg

bp = Blueprint()
bp.name = "Edit announcement"


@bp.on.message(text="Редактировать объявление")
@bp.on.message(payload={"cmd": "edit_announcement"})
async def edit_announcement(message: Message):
    keyboard = get_announcements(await Announcement.all(), 3)
    await message.answer("Выбери объяву.", keyboard=keyboard)
    await bp.state_dispenser.set(message.peer_id, AnnouncementEditingStates.GET_ID)


@bp.on.message(state=AnnouncementEditingStates.GET_ID)
async def get_id(message: Message, storage):
    storage['ad'] = ad = await Announcement.get(id=json.loads(message.payload)['id'])

    formatted = msg % (str(ad.price), ad.text)

    await message.answer(
        message=f"Текущее объявление выглядит так: \n\n{formatted}",
        keyboard=ANNOUNCEMENT_EDITING_KEYBOARD
    )
    await bp.state_dispenser.set(message.peer_id, AnnouncementEditingStates.GET_ACTION)


@bp.on.message(payload_map={"edit":str}, state=AnnouncementEditingStates.GET_ACTION)
async def get_action(message: Message, storage):
    action = json.loads(message.payload)['edit']
    storage['action'] = action

    await message.answer(message="Теперь пиши новое значение. Value. Ну новую хуйню всю епт")
    await bp.state_dispenser.set(message.peer_id, AnnouncementEditingStates.GET_VALUE)


@bp.on.message(state=AnnouncementEditingStates.GET_VALUE)
async def get_value(message: Message, storage):
    ad: Announcement = storage['ad']
    await ad.update_from_dict({storage['action']: message.text})
    await ad.save()

    formatted = msg % (str(ad.price), ad.text)

    await message.answer(
        message=f"Всё. Новое объявление: \n\n{formatted}",
        keyboard=BACK_TO_MENU)
    await bp.state_dispenser.delete(message.peer_id)

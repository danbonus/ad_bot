import json

from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from models.group import Group
from utils.keyboard import BACK_TO_MENU, get_groups, CONFIRMATION_KEYBOARD
from utils.states import GroupDeletionStates

bp = Blueprint()
bp.name = "Remove group"


@bp.on.message(text="Удалить группу из БД")
@bp.on.message(payload={"cmd": "remove_group"})
async def remove_group(message: Message, no_section_storage):
    api = no_section_storage['announcers'][message.from_id]
    text, keyboard = await get_groups(api, await Group.all())
    text += "При нажатии на кнопку выбранная группа будет удалена."
    await message.answer(text, keyboard=keyboard)
    await bp.state_dispenser.set(message.peer_id, GroupDeletionStates.GET_GROUP)


@bp.on.message(state=GroupDeletionStates.GET_GROUP)
async def get_group(message: Message, storage):
    storage['uid'] = json.loads(message.payload)['group_id']
    await message.answer("Да/нет?", keyboard=CONFIRMATION_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, GroupDeletionStates.CONFIRMATION_STATE)


@bp.on.message(state=GroupDeletionStates.CONFIRMATION_STATE)
async def confirmation(message: Message, storage):
    if json.loads(message.payload)['status']:
        group = await Group.get(uid=storage['uid'])
        await group.delete()
        await message.answer("всё.", keyboard=BACK_TO_MENU)
    else:
        await message.answer('ну и пошел нахуй', keyboard=BACK_TO_MENU)
    await bp.state_dispenser.delete(message.peer_id)

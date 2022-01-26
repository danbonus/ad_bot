from urllib.parse import urlparse

from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from models.group import Group
from utils.keyboard import BACK_TO_MENU
from utils.states import GroupAdditionStates

bp = Blueprint()
bp.name = "Add group"


@bp.on.message(text="Добавить группу")
@bp.on.message(payload={"cmd": "add_group"})
async def create_announcement(message: Message):
    await bp.state_dispenser.set(message.peer_id, GroupAdditionStates.GET_LINK)
    await message.answer("Скинь ссылку.", keyboard=BACK_TO_MENU)


@bp.on.message(state=GroupAdditionStates.GET_LINK)
async def get_link(message: Message, no_section_storage):
    link = urlparse(message.text).path[1::]
    api = no_section_storage['announcers'][message.from_id]
    group = await api.groups.get_by_id(group_id=link)
    await Group.create(uid=-group[0].id)
    await bp.state_dispenser.delete(message.peer_id)
    return "Готово. Ты спецом такую уебскую группу выбрал? Кринж.. бляяя. "

from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from utils.keyboard import MENU_KEYBOARD, ANNOUNCEMENT_KEYBOARD, GROUPS_KEYBOARD

bp = Blueprint()
bp.name = "Menu"


@bp.on.private_message(payload={"cmd": "groups_menu"})
async def announcements_menu(message: Message):
    if message.state_peer:
        await bp.state_dispenser.delete(message.peer_id)
    await message.answer("Вот клава групп.", keyboard=GROUPS_KEYBOARD)


@bp.on.private_message(payload={"cmd": "announcements_menu"})
async def announcements_menu(message: Message):
    if message.state_peer:
        await bp.state_dispenser.delete(message.peer_id)
    await message.answer("Вот клава объяв.", keyboard=ANNOUNCEMENT_KEYBOARD)


@bp.on.private_message()
@bp.on.private_message(payload={"cmd": "menu"})
async def menu(message: Message):
    if message.state_peer:
        await bp.state_dispenser.delete(message.peer_id)
    await message.answer("Вот клава.", keyboard=MENU_KEYBOARD)

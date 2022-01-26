import json

from vkbottle.bot import Blueprint
from vkbottle.bot import Message

from models.announcement import Announcement
from models.group import Group
from utils.keyboard import BACK_TO_MENU
from utils.states import UtilsStates
from utils.storage import CtxStorage
from utils.utils import send_ad

bp = Blueprint()
bp.name = "Send ad"


@bp.on.private_message(payload_map={"id":int}, state=UtilsStates.SEND_STATE)
async def send(message: Message, no_section_storage: CtxStorage):
    ad_id = json.loads(message.payload)['id']
    announcement = await Announcement.get(id=ad_id)
    api = no_section_storage['announcers'][announcement.announcer_uid]
    await send_ad(api, announcement, await Group.all())
    await message.answer("Выполнено!", keyboard=BACK_TO_MENU)

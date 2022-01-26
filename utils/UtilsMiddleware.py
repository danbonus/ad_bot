from vkbottle import BaseMiddleware
from vkbottle.bot import Message

from utils.storage import CtxStorage


class UtilsMiddleware(BaseMiddleware[Message]):
    async def pre(self):
        storage = CtxStorage(section=self.event.from_id)
        self.send({
            'storage': storage,
            'no_section_storage': CtxStorage()
        })

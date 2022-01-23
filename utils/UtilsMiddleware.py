from vkbottle import BaseMiddleware
from utils.storage import CtxStorage
from vkbottle.bot import Message


class UtilsMiddleware(BaseMiddleware[Message]):
    async def pre(self):
        storage = CtxStorage(section=self.event.from_id)
        print('хуй пизда')
        self.send({
            'storage': storage
        })

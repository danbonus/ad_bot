from asyncio import gather

from vkbottle import PhotoToAlbumUploader
from vkbottle.bot import Blueprint
from vkbottle.bot import Message
from vkbottle.http import AiohttpClient

from models.announcement import Announcement
from utils.keyboard import BACK_TO_MENU
from utils.states import AnnouncementCreationStates
from utils.storage import CtxStorage
from utils.utils import chunks

bp = Blueprint()
bp.name = "Create announcement"


@bp.on.message(text="Создать объявление")
@bp.on.message(payload={"cmd": "create_announcement"})
async def create_announcement(message: Message):
    await bp.state_dispenser.set(message.peer_id, AnnouncementCreationStates.GET_NAME)
    await message.answer("Введи название объявления.", keyboard=BACK_TO_MENU)


@bp.on.message(state=AnnouncementCreationStates.GET_NAME)
async def get_name(message: Message, storage):
    storage["name"] = message.text
    await bp.state_dispenser.set(message.peer_id, AnnouncementCreationStates.GET_TEXT)
    return "Ок, название получил. Ты спецом такое уебское придумал? Кринж.. бляяя. Вводи текст объявы"


@bp.on.message(state=AnnouncementCreationStates.GET_TEXT)
async def get_text(message: Message, storage):
    await bp.state_dispenser.set(message.peer_id, AnnouncementCreationStates.GET_ATTACHMENTS)

    storage["text"] = message.text
    return "Ага, теперь и эту хуйню записал. Пиздец, чем я занимаюсь на старость лет? " \
           "Присылай картинки к объяве."


@bp.on.message(state=AnnouncementCreationStates.GET_ATTACHMENTS)
async def get_attachments(message: Message, storage):
    await bp.state_dispenser.set(message.peer_id, AnnouncementCreationStates.GET_PRICE)
    await message.answer("Присылай цену")

    msg = await bp.api.messages.get_by_conversation_message_id(
        peer_id=message.peer_id,
        conversation_message_ids=[message.conversation_message_id]
    )

    attachments = msg.items[0].get_photo_attachments()
    if attachments:
        api = CtxStorage()['announcers'][message.from_id]

        album = await api.photos.create_album(
            title=storage['name'],
            privacy_view="only_me"
        )

        tasks = []
        attachments_list = []
        for attachment in attachments:
            tasks.append(
                AiohttpClient().request_content(url=attachment.sizes[-1].url)
                )

        attachments_list.extend(await gather(*tasks))

        print("Fetched!")
        uploader = PhotoToAlbumUploader(api=api)

        tasks = []
        for i in chunks(attachments_list, 5):
            tasks.append(uploader.upload(album_id=album.id, paths_like=i))

        storage['attachments'] = []
        for i in await gather(*tasks):
            storage["attachments"].extend(i)
    else:
        return 'Ок, без картинок'


@bp.on.message(state=AnnouncementCreationStates.GET_PRICE)
async def get_price(message: Message, storage):
    await bp.state_dispenser.set(message.peer_id, AnnouncementCreationStates.GET_TIME)

    if not message.text.isdigit():
        return 'Пришли только цену. Цифры.'
    storage["price"] = message.text
    return "В какое время рассылать? Пример: 16:00, 20:00. Да, можно через запятую"


@bp.on.message(state=AnnouncementCreationStates.GET_TIME)
async def get_time(message: Message, storage):
    await bp.state_dispenser.delete(message.peer_id)
    announce_time = [i.strip() for i in message.text.split(",")]

    await Announcement.create(
        name=storage["name"],
        text=storage['text'],
        attachments=storage['attachments'],
        time=announce_time,
        price=storage['price'],
        announcer_uid=message.from_id
    )
    return "Ну всё, блять, молодец. Создано."

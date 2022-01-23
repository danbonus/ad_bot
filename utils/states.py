from vkbottle import BaseStateGroup


class MenuStates(BaseStateGroup):
    ANNOUNCEMENTS = 0
    GROUPS = 1
    LOG = 2


class AnnouncementCreationStates(BaseStateGroup):
    GET_NAME = 3
    GET_TEXT = 4
    GET_ATTACHMENTS = 5
    GET_PRICE = 6
    GET_TIME = 7

from vkbottle import BaseStateGroup


class MenuStates(BaseStateGroup):
    ANNOUNCEMENTS = 0
    GROUPS = 1
    LOG = 2


class AnnouncementStates(BaseStateGroup):
    CREATE_ANNOUNCEMENT = 5
    VIEW_ANNOUNCEMENTS = 6
    ARCHIVE_ANNOUNCEMENT = 7


class AnnouncementCreationStates(BaseStateGroup):
    GET_NAME = 8
    GET_TEXT = 9
    GET_ATTACHMENTS = 10
    GET_PRICE = 11
    GET_TIME = 12

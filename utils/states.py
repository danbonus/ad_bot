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


class AnnouncementDeletionStates(BaseStateGroup):
    GET_ID = 8
    CONFIRMATION_STATE = 9


class UtilsStates(BaseStateGroup):
    SEND_STATE = 10


class GroupAdditionStates(BaseStateGroup):
    GET_LINK = 11


class GroupDeletionStates(BaseStateGroup):
    GET_GROUP = 12
    CONFIRMATION_STATE = 13
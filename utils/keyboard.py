from typing import Optional

from vkbottle import Keyboard as RootKeyboard
from vkbottle import KeyboardButtonColor, ABCAction
from vkbottle import Text
from vkbottle.tools.dev.keyboard.button import KeyboardButton


class Keyboard(RootKeyboard):
    def add(self, action: ABCAction, row: int = 5, color: Optional[KeyboardButtonColor] = None) -> "Keyboard":
        if not len(self.buttons):
            self.row()
        if len(self.buttons[-1]) == row:
            self.row()
        button = KeyboardButton.from_typed(action, color)
        self.buttons[-1].append(button)
        return self

    def __add__(self, other_keyboard: RootKeyboard):
        temp_keyboard = Keyboard(one_time=self.one_time, inline=self.inline)
        temp_keyboard.buttons.extend(self.buttons)
        temp_keyboard.buttons.extend(other_keyboard.buttons)
        return temp_keyboard


MENU_KEYBOARD = (
    Keyboard()
    .add(Text("Объявления", {"cmd": "announcements_menu"}))
    .row()
    .add(Text("Группы", {"cmd": "groups_menu"}))
    .row()
    .add(Text("Лог", {"cmd": "view_log"}))
).get_json()


ANNOUNCEMENT_KEYBOARD = (
    Keyboard()
    .add(Text("Создать объявление", {"cmd": "create_announcement"}))
    .row()
    .add(Text("Посмотреть объявления", {"cmd": "show_announcements"}))
    .row()
    .add(Text("Удалить объявление", {"cmd": "delete_announcement"}))
).get_json()


GROUPS_KEYBOARD = (
    Keyboard()
    .add(Text("Добавить группу", {"cmd": "add_group"}))
    .row()
    .add(Text("Посмотреть список групп", {"cmd": "show_groups"}))
    .row()
    .add(Text("Удалить группу из БД", {"cmd": "remove_group"}))
)

BACK_TO_MENU = Keyboard()
BACK_TO_MENU.add(Text("Вернуться в меню", {"cmd": "menu"}))
BACK_TO_MENU = BACK_TO_MENU.get_json()


CONFIRMATION_KEYBOARD = (
    Keyboard()
    .add(Text("Да", {"status": True}))
    .add(Text("Нет", {"status": False}))
).get_json()


def get_announcements_to_delete(announcements, row=3):
    keyboard = Keyboard()

    for ad in announcements:
        keyboard.add(Text(ad.name, {"id": ad.id}), row=row)

    return keyboard


def get_announcements_to_show(announcements, row=3):
    text = ""
    keyboard = Keyboard()

    for i, ad in enumerate(announcements):
        text += f"{i}) {ad.name} / {ad.price}р / {', '.join(ad.time)}\n\n"
        keyboard.add(Text(ad.name, {"id": ad.id}), row=row)

    text += "При нажатии на кнопку выбранная объява будет разослана. Не переборщи"
    return text, keyboard


async def get_groups(api, groups, row=2):
    text = ""
    keyboard = Keyboard()

    for i, group in enumerate(groups):
        group_info = await api.groups.get_by_id(group_id=abs(group.uid), fields="members_count")
        group_info = group_info[0]

        text += f"{i+1}) [club{group_info.id}|{group_info.name}] / {group_info.members_count} участников\n\n"
        keyboard.add(Text(group_info.name[:40], {"group_id": group.uid}), row=row)

    return text, keyboard

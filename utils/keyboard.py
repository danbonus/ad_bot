from vkbottle import KeyboardButtonColor, Text, Keyboard


MENU_KEYBOARD = (
    Keyboard()
    .add(Text("Объявления", {"cmd": "announcements"}))
    .row()
    .add(Text("Группы", {"cmd": "groups"}))
    .row()
    .add(Text("Лог", {"cmd": "view_log"}))
).get_json()


ANNOUNCEMENT_KEYBOARD = (
    Keyboard()
    .add(Text("Создать объявление", {"cmd": "create_announcement"}))
    .row()
    .add(Text("Просмотреть объявления", {"cmd": "view_announcements"}))
    .row()
    .add(Text("Архивировать объявление", {"cmd": "archive_announcement"}))
).get_json()

BACK_TO_MENU = Keyboard()
BACK_TO_MENU.add(Text("Вернуться в меню", {"cmd": "back"}))
BACK_TO_MENU = BACK_TO_MENU.get_json()

from tortoise import Tortoise


async def init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models.announcement', 'models.announcer', 'models.group']}
    )
    await Tortoise.generate_schemas()
    #test_status = await Status.create(name="basic_status", description="Обычный статус.", text="Беу. Вне зоны доступа. Хз почему.")
    #await Status(name="basic_status").save()

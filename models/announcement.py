from tortoise.models import Model
from tortoise import fields


class Announcement(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField(required=True)
    text = fields.TextField()
    attachments = fields.JSONField()
    time = fields.DatetimeField()
    price = fields.IntField()

    class Meta:
        model = "Announcement"
        fields = ('name', 'text', 'price', 'attachments', 'time')

    def __str__(self):
        return self.name

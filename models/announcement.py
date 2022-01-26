from tortoise import fields
from tortoise.models import Model


class Announcement(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField(required=True)
    text = fields.TextField()
    attachments = fields.JSONField()
    time = fields.JSONField()
    price = fields.IntField()
    announcer_uid = fields.IntField()

    class Meta:
        model = "Announcement"
        fields = ('name', 'text', 'price', 'attachments', 'time')

    def __str__(self):
        return self.name

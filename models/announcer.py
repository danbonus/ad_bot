from tortoise import fields
from tortoise.models import Model


class Announcer(Model):
    id = fields.IntField(pk=True)
    uid = fields.IntField()
    token = fields.TextField()

    class Meta:
        model = "Announcer"
        fields = ('uid', 'token')

    def __str__(self):
        return self.uid

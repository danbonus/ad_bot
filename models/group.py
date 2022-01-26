from tortoise import fields
from tortoise.models import Model


class Group(Model):
    id = fields.IntField(pk=True)
    uid = fields.IntField(required=True)

    class Meta:
        model = "Groups"
        fields = ('uid',)

    def __str__(self):
        return self.uid

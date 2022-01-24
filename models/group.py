from tortoise.models import Model
from tortoise import fields


class Group(Model):
    id = fields.IntField(pk=True)
    uid = fields.IntField(required=True)

    class Meta:
        model = "Groups"
        fields = ('uid',)

    def __str__(self):
        return self.uid

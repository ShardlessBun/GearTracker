import typing

from marshmallow import Schema, fields, ValidationError, post_load

from GearTracker.objects.objects import Equipment


class ValueField(fields.Field):
    def _deserialize(
        self,
        value: typing.Any,
        attr: str | None,
        data: typing.Mapping[str, typing.Any] | None,
        **kwargs,
    ):
        if isinstance(value, int) or isinstance(value, float) or isinstance(value, dict):
            return value
        else:
            raise ValidationError('Field should be an int, float, or dict')


class SpecialValueField(fields.Field):
    def _deserialize(
        self,
        value: typing.Any,
        attr: str | None,
        data: typing.Mapping[str, typing.Any] | None,
        **kwargs,
    ):
        if isinstance(value, int) or isinstance(value, str):
            return value
        else:
            raise ValidationError('Field should be an int or str')


class JobSchema(Schema):
    id = fields.Integer(data_key='id', required=True)
    abbreviation = fields.String(data_key='abbrev', required=True)


class EquipmentSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    description = fields.String()
    param0 = fields.Integer(allow_none=True)
    param1 = fields.Integer(allow_none=True)
    param2 = fields.Integer(allow_none=True)
    param3 = fields.Integer(allow_none=True)
    param4 = fields.Integer(allow_none=True)
    param5 = fields.Integer(allow_none=True)
    param0Value = fields.Integer(load_default=0)
    param1Value = fields.Integer(load_default=0)
    param2Value = fields.Integer(load_default=0)
    param3Value = fields.Integer(load_default=0)
    param4Value = fields.Integer(load_default=0)
    param5Value = fields.Integer(load_default=0)
    maxParams = fields.Dict(keys=fields.Str(), values=fields.Int())
    advancedMelding = fields.Bool()
    block = fields.Integer()
    blockRate = fields.Integer()
    canBeHq = fields.Bool()
    damageMag = fields.Integer()
    damagePhys = fields.Integer()
    defenseMag = fields.Integer()
    defensePhys = fields.Integer()
    delay = fields.Integer()
    iconId = fields.Integer()
    iconPath = fields.Url(relative=True)
    itemLevel = fields.Integer()
    itemSpecialBonus = fields.Dict(keys=fields.String(), values=SpecialValueField(), allow_none=True)
    itemSpecialBonusParam = fields.Integer()
    level = fields.Integer()
    materiaSlotCount = fields.Integer()
    materializeType = fields.Integer()
    PVP = fields.Bool()
    rarity = fields.Integer()
    slotCategory = fields.Integer()
    unique = fields.Bool()
    untradable = fields.Bool()
    weapon = fields.Bool()
    canCustomize = fields.Bool()
    slotName = fields.String()
    jobName = fields.String()
    itemUICategory = fields.Integer()
    jobCategory = fields.Integer()

    @post_load
    def make_equipment(self, data, **kwargs):
        return Equipment(**data)


class ParamSchema(Schema):
    id = fields.String(allow_none=True)
    name = fields.String()
    units = fields.String(allow_none=True)
    value = ValueField()


class GearsetSchema(Schema):
    id = fields.String()
    jobAbbrev = fields.String()
    jobIconPath = fields.Url(relative=True)
    clanName = fields.String()
    isOwner = fields.Boolean()
    name = fields.String()
    lastUpdate = fields.DateTime()
    minItemLevel = fields.Integer()
    maxItemLevel = fields.Integer()
    minMateriaTier = fields.Integer()
    maxMateriaTier = fields.Integer()
    materia = fields.Dict(
        keys=fields.String(),
        values=fields.Dict(
            keys=fields.String(),
            values=fields.Integer()
        )
    )
    totalParams = fields.List(fields.Nested(ParamSchema()))
    # buffs =
    # relics =
    patch = fields.Float()
    notes = fields.String(allow_none=True)
    job = fields.Integer()
    clan = fields.Integer()
    weapon = fields.Integer()
    head = fields.Integer()
    body = fields.Integer()
    hands = fields.Integer()
    legs = fields.Integer()
    feet = fields.Integer()
    offHand = fields.Integer(allow_none=True)
    ears = fields.Integer()
    neck = fields.Integer()
    wrists = fields.Integer()
    fingerL = fields.Integer()
    fingerR = fields.Integer()
    food = fields.Integer()
    medicine = fields.Integer(allow_none=True)

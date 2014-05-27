from mongoengine import EmbeddedDocument, IntField, FloatField, Document, \
    StringField


# class ChargedMeson24c(models.Model):
#     source = models.CharField(max_length=20)
#     sink = models.CharField(max_length=20)
#     m_l = models.FloatField()  # light sea mass
#     mass_1 = models.FloatField()
#     mass_2 = models.FloatField()
#     charge_1 = models.IntegerField()
#     charge_2 = models.IntegerField()
#     config_number = models.IntegerField(db_index=True)
#
#
# class TimeSlice(models.Model):
#     t = models.IntegerField()
#     re = models.FloatField()
#     im = models.FloatField()
#     meson = models.ForeignKey(ChargedMeson24c, related_name='data',
#                               db_index=True)


class PionLEC(Document):
    LS = FloatField()
    B0 = FloatField()
    F0 = FloatField()
    L64 = FloatField()
    L85 = FloatField()
    L4 = FloatField()
    L5 = FloatField()
    m_res = FloatField()
    miu = FloatField()
    config_number = IntField()


class KaonLEC(Document):
    M2 = FloatField()
    A3 = FloatField()
    A4 = FloatField()
    delta_m_res = FloatField()
    config_number = IntField()


class TimeSlice(EmbeddedDocument):
    t = IntField()
    re = FloatField()
    im = FloatField()


class ChargedMeson24c(Document):
    source = StringField(max_length=20)
    sink = StringField(max_length=20)
    m_l = FloatField()  # light sea mass
    mass_1 = FloatField()
    mass_2 = FloatField()
    charge_1 = IntField()
    charge_2 = IntField()
    config_number = IntField()
from mongoengine import Document, FloatField, IntField


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
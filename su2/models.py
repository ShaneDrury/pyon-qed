# Create your models here.
from mongoengine import Document, FloatField, IntField


class PionLECSU2(Document):
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


class KaonLECSU2(Document):
    M2 = FloatField()
    A_3 = FloatField()
    A_4 = FloatField()
    m_s = FloatField()
    config_number = IntField()
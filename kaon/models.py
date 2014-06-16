from mongoengine import Document, FloatField, IntField


class KaonLEC(Document):
    M2 = FloatField()
    A3 = FloatField()
    A4 = FloatField()
    delta_m_res = FloatField()
    config_number = IntField()
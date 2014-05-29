from mongoengine import EmbeddedDocument, IntField, FloatField, Document, \
    StringField, EmbeddedDocumentField, ListField


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
    #im = FloatField()  # don't actually need this


class Correlator(EmbeddedDocument):
    """
    A Correlator is a collection of time slices for one config number
    """
    config_number = IntField()
    data = ListField(EmbeddedDocumentField(TimeSlice))


class ChargedMeson24c(Document):
    """
    A Meson is a collection of Correlators and meta data
    """
    source = StringField(max_length=20)
    sink = StringField(max_length=20)
    m_l = FloatField()  # light sea mass
    mass_1 = FloatField()
    mass_2 = FloatField()
    charge_1 = IntField()
    charge_2 = IntField()
    correlators = ListField(EmbeddedDocumentField(Correlator))

    meta = {
        'allow_inheritance': True,
        'index_background': True,
        'indexes': [('+m_l', '+source', '+sink')]
    }
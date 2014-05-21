from django.db import models


class ChargedMeson24c(models.Model):
    source = models.CharField(max_length=20)
    sink = models.CharField(max_length=20)
    m_l = models.FloatField()  # light sea mass
    mass_1 = models.FloatField()
    mass_2 = models.FloatField()
    charge_1 = models.IntegerField()
    charge_2 = models.IntegerField()
    config_number = models.IntegerField(db_index=True)


class TimeSlice(models.Model):
    t = models.IntegerField()
    re = models.FloatField()
    im = models.FloatField()
    meson = models.ForeignKey(ChargedMeson24c, related_name='data',
                              db_index=True)


class PionLEC(models.Model):
    LS = models.FloatField()
    B0 = models.FloatField()
    F0 = models.FloatField()
    L64 = models.FloatField()
    L85 = models.FloatField()
    L4 = models.FloatField()
    L5 = models.FloatField()
    m_res = models.FloatField()
    miu = models.FloatField()
    config_number = models.IntegerField(db_index=True)


class KaonLEC(models.Model):
    M2 = models.FloatField()
    A3 = models.FloatField()
    A4 = models.FloatField()
    delta_m_res = models.FloatField()
    config_number = models.IntegerField(db_index=True)


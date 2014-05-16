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
    t = models.IntegerField(db_index=True)
    re = models.FloatField()
    im = models.FloatField()
    meson = models.ForeignKey(ChargedMeson24c, related_name='data')
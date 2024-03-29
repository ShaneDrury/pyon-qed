"""
Define your models here. These define the structure of the tables in the
database and use Django's syntax.
"""
from django.db import models


class ChargedMeson32c(models.Model):
    source = models.CharField(max_length=20)
    sink = models.CharField(max_length=20)
    m_l = models.FloatField()
    mass_1 = models.FloatField()
    mass_2 = models.FloatField()
    charge_1 = models.IntegerField()
    charge_2 = models.IntegerField()
    config_number = models.IntegerField(db_index=True)


class TimeSlice(models.Model):
    t = models.IntegerField(db_index=True)
    re = models.FloatField()
    im = models.FloatField()
    meson = models.ForeignKey(ChargedMeson32c, related_name='data')


# class LEC(models.Model):

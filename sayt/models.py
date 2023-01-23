from collections import OrderedDict

from django.db import models


# Create your models here.

def choises(type):
    if type == 'tarif':
        return [
            ("Umra", "Umra"),
            ("Haj", "Haj"),

        ]
    elif type == 'price':
        return [

            ("$", "$"),
            ("UZS", "UZS"),
        ]


class Tarif(models.Model):
    type = models.CharField(max_length=128, choices=choises('tarif'))
    paket = models.CharField(max_length=128)
    start_date = models.DateField()
    end_date = models.DateField()
    max_place = models.IntegerField()
    duration = models.IntegerField()
    eating = models.CharField(max_length=256)
    distance = models.IntegerField()
    room = models.IntegerField()
    price_type = models.CharField(max_length=10, choices=choises("price"))
    price = models.IntegerField()
    img = models.ImageField(upload_to="tarif")

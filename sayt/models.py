from collections import OrderedDict

from django.db import models

from api.models import User


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
    # paket_uz = models.CharField(max_length=128)
    # paket_ru = models.CharField(max_length=128)
    # paket_en = models.CharField(max_length=128)
    start_date = models.DateField()
    end_date = models.DateField()
    max_place = models.IntegerField()
    duration = models.IntegerField()
    eating = models.CharField(max_length=256)
    distance = models.IntegerField()
    room = models.IntegerField()
    price_type = models.CharField(max_length=10, choices=choises("price"))
    price = models.IntegerField()
    img = models.ImageField(upload_to="tarif", blank=True, null=True)
    is_activa = models.BooleanField(default=True)

    def __str__(self):
        return self.type


class News(models.Model):
    """ nomi -name """
    name = models.CharField(max_length=256)
    '''vaqti va sana`si-date'''
    date = models.DateField(auto_now_add=True)

    title = models.CharField(max_length=512)

    short_desc = models.TextField()

    desc = models.TextField()

    '''rasmi-img'''

    img = models.ImageField(upload_to="news", blank=True, null=True)

    def __str__(self):
        return self.name


# qo'shilgan joyi
class TarifBron(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, db_constraint=False)
    tarif = models.ForeignKey(Tarif, on_delete=models.DO_NOTHING, null=True, db_constraint=False)
    status = models.IntegerField(choices=[
        (0, "Bron qilingan"),
        (1, "To'lov qilingan"),
    ], default=0)
    create_at = models.DateTimeField(auto_now_add=True)

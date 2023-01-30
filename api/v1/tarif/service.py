from collections import OrderedDict

from base.fomats import format_tarif


def format_bron(data):
    return OrderedDict([
        ('user', data.user.mobile),
        ('tarif', format_tarif(data.tarif)),
        ("status", data.status),
        ("create_date", data.create_at)
    ])


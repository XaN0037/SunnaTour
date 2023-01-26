from api.v1.tarif.views import format_tarif
from base.slavar import TXT
from sayt.models import Tarif


def header(lan):
    return {
        "haj": TXT['HAJ'][lan],
        "umra": TXT['UMRA'][lan],
        "zt": TXT['ZT'][lan],
        "hadis": TXT['HADIS'][lan]
    }

def footer(lan):
    pass

def haj_keys(lan):
    return {

    }

def index(lang='uz'):
    cont1 = {
        "title": TXT['c1Title'][lang]
    }

    return {
        "header": header(lang),
        "cont1": cont1

    }


def haj(lan):
    tarif = [format_tarif(x) for x in Tarif.objects.filter(is_activa=True, type="Haj").order_by("-pk")[:3]]


    return {
        "header": header(lan),
        "tarif": {
            "caption": TXT['HAJYIL'][lan],
            "keys": haj_keys(lan),
            "data": tarif
        }
    }

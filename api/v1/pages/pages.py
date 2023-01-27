from api.v1.tarif.views import format_tarif
from base.slavar import TXT
from sayt.models import Tarif


def header(lan):
    return {
        "haj": TXT['HAJ'][lan],
        "umra": TXT['UMRA'][lan],
        "zt": TXT['ZT'][lan],
        "hadis": TXT['HADIS'][lan],
        "aviabilet": TXT['AVIABILET'][lan],
        "malumotlar": TXT['MALUMOTLAR'][lan],
        "tulov": TXT['TULOV'][lan],

    }

def footer(lan):
    pass

def haj_keys(lan):
    return {

    }

def index(lang='uz'):
    cont1 = {
        "title": TXT['c1Title'][lang],
        "hajyil": TXT['HAJYIL'][lang],
        "mehmonhona": TXT['MEXMONXONALAR'][lang],
        "avia": TXT['AVIACHIPTA'][lang],
        "turkiya": TXT['TURKIYA'][lang],
        "sunnatour": TXT['SUNNATOURMAKS'][lang],
        "payme": TXT['PAYME'][lang],

    }
    cont2 = {
        "jonliefir": TXT['MAKKA'][lang],
        "haj2023": TXT['HAJ2023'][lang],
        "dastur": TXT['DASTUR'][lang],
        "haqida": TXT['HAJHAQIDA'][lang],
        "shartnoma": TXT['SHARTNOMALAR'][lang],
        "trening": TXT['TRENING'][lang],
        "yul": TXT['YULDA'][lang],
        "marosim": TXT['MAROSIM'][lang],
        "uy": TXT['UY'][lang],


    }
    cont3 = {
        "reys": TXT['REYSMEHMONXONA'][lang],
        "avia": TXT['AVIACHIPTA'][lang],
        "mexmonxona": TXT['MEXMONXONALAR'][lang],
        "uchish": TXT['UCHISH'][lang],
        "kelish": TXT['KELISH'][lang],
        "sana": TXT['SANA'][lang],
        "yulovchi": TXT['YULOVCHI'][lang],
        "chipta": TXT['CHIPTATOP'][lang],
        "mexmon": TXT['MEHMONXONA'][lang],



    }
    cont4 = {
        "yangilik": TXT['YANGILIK'][lang],
        "yangilik": TXT['YANGILIK'][lang],


    }

    return {
        "header": header(lang),
        "cont1": cont1,
        "cont2": cont2,
        "cont3": cont3,

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

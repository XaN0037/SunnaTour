from api.v1.tarif.views import format_tarif
from base.slavar import TXT, BIGTXTNAME, BIGTXT, KOMPANY
from sayt.models import Tarif, News
from api.v1.news.views import format


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
    return {

        "shart": TXT['SHARTNOMA'][lan],
        "maxfiy": TXT['MAXFIYLIK'][lan],
    }


def haj_keys(lan):
    return {

    }


def index(lang='uz'):
    news = [format(x) for x in News.objects.all().order_by("-pk")[:10]]
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
        "musulmon": TXT['MUSULMONMEHMONXONA'][lang],

    }
    cont4 = {
        "yangilik": TXT['YANGILIK'][lang],

    }

    return {
        "header": header(lang),
        "cont1": cont1,
        "cont2": cont2,
        "cont3": cont3,
        "cont4": cont4,
        "news": news,
        "footer": footer(lang),

    }


def haj(lan='uz'):
    tarif = [format_tarif(x) for x in Tarif.objects.filter(is_activa=True, type="Haj").order_by("-pk")[:3]]
    cont1 = {
        "eko": TXT['EKONOMKLASS'][lan],
        "o'rta": TXT['URTAKLASS'][lan],
        "yuqori": TXT['YUQORIKLASS'][lan],
        "hamjoy": TXT['HAMMAJOYLAR'][lan],
        "qoljoy": TXT['QOLGANJOYLAR'][lan],
        "davom": TXT['DAVOMIYLIGI'][lan],
        "metr": TXT['MASOFA'][lan],
        "xona": TXT['TURARJOY'][lan],
        "narx": TXT['NARXI'][lan],
        "buyurtma": TXT['BUYURTMA'][lan],

    }
    cont2 = {
        "komp": TXT['KOMPHAQIDA'][lan],
    }
    cont3 = {
        "haqimizda": TXT['BIZHAQIMIZDA'][lan],

    }
    return {
        "header": header(lan),
        "tarif": {
            "caption": TXT['HAJYIL'][lan],
            "keys": haj_keys(lan),
            "data": tarif
        },
        "cont1": cont1,
        "footer": footer(lan),
    }


def umra(lan='uz'):
    tarif = [format_tarif(x) for x in Tarif.objects.filter(is_activa=True, type="Umra").order_by("-pk")[:3]]

    return {
        "header": header(lan),
        "tarif": {
            "caption": TXT['UMRA'][lan],
            "keys": haj_keys(lan),
            "data": tarif
        },
        "footer": footer(lan),
    }


def ziyotur(lan='uz'):
    cont1 = {
        "ziyotur": TXT['ZT'][lan],
    }
    return {
        "header": header(lan),
        "cont1": cont1,
        "footer": footer(lan),
    }


def hadis(lan='uz'):
    cont1 = {
        "hadisname1": BIGTXTNAME['HADIS1'][lan],
        "hadis1": BIGTXT['HADIS1'][lan],

        "hadisname2": BIGTXTNAME['HADIS2'][lan],
        "hadis2": BIGTXT['HADIS2'][lan],

        "hadisname3": BIGTXTNAME['HADIS3'][lan],
        "hadis3": BIGTXT['HADIS3'][lan],

        "hadisname4": BIGTXTNAME['HADIS4'][lan],
        "hadis4": BIGTXT['HADIS4'][lan],

        "hadisname5": BIGTXTNAME['HADIS5'][lan],
        "hadis5": BIGTXT['HADIS5'][lan],

        "hadisname6": BIGTXTNAME['HADIS6'][lan],
        "hadis6": BIGTXT['HADIS6'][lan],

    }
    return {
        "header": header(lan),
        "cont1": cont1,
        "footer": footer(lan),
    }


def aviobilet(lan='uz'):
    cont1 = {
        "reys": TXT['REYSMEHMONXONA'][lan],
        "avia": TXT['AVIACHIPTA'][lan],
        "uchish": TXT['UCHISH'][lan],
        "kelish": TXT['KELISH'][lan],
        "sana": TXT['SANA'][lan],
        "yulovchi": TXT['YULOVCHI'][lan],
        "chipta": TXT['CHIPTATOP'][lan],
        "mexmon": TXT['MEHMONXONA'][lan],


    }

    cont2 = {
        "arzon": TXT['ARZON'][lan],
        "ishonch": TXT['ISHONCHLI'][lan],
        "tezkor": TXT['TEZKOR'][lan],
        "global": TXT['GLOBAL'][lan],
        "tez": TXT['TEZ'][lan],
        "ijtimoiy": TXT['IJTIMOIY'][lan],
        "chegirma": TXT['CHEGIRMA'][lan],
        "obuna": TXT['OBUNA'][lan],
        "offerta": TXT['OFFERTA'][lan],
    }
    return {
        "header": header(lan),
        "cont1": cont1,
        "cont2": cont2,

        "footer": footer(lan),
    }


def kompaniya(lan='uz'):
    cont1 = {
        "kom": TXT['KOMHAQIDA'][lan],
        'adress': KOMPANY['MANZIL'][lan],
        'farq': KOMPANY['FARQ'][lan],
        'dastur': KOMPANY['DASTUR'][lan],
        'shifo': KOMPANY['SHIFO'][lan],
        'faoliyat': KOMPANY['FAOLIYAT'][lan],
        'manzil2': KOMPANY['MANZIL2'][lan],
        'til': KOMPANY['TIL'][lan],
        'maruza': KOMPANY['MARUZA'][lan],
        'halolmexmon': KOMPANY['HALOLMEXMON'][lan],
        'tulov': KOMPANY['TULOV'][lan],
        'sayt': KOMPANY['SAYT'][lan],
        'narx': KOMPANY['NARX'][lan],
        'osago': KOMPANY['OSAGO'][lan],
        'tanlov': KOMPANY['TANLOV'][lan],
        'oxirgi': KOMPANY['OXIRI'][lan],

    }
    return {
        "header": header(lan),
        "cont1": cont1,
        "footer": footer(lan),
    }


def malumot(lan='uz'):
    cont1 = {

    }
    return {
        "header": header(lan),
        "cont1": cont1,
        "footer": footer(lan),
    }


def tulov(lan='uz'):
    cont1 = {

    }
    return {
        "header": header(lan),
        "cont1": cont1,
        "footer": footer(lan),
    }


def login(lan='uz'):
    cont1 = {

    }
    return {
        "header": header(lan),
        "cont1": cont1,
        "footer": footer(lan),
    }

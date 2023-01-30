from collections import OrderedDict


def _avto_formater(data=None, model=True, **kwargs):
    l = []
    if model:
        for i in data.dir():

            if i == "_state" or i == "dir" or i == 'user':
                continue
            elif i == "module" or i == "_password":
                break
            elif i == 'img':
                l.append(
                    (f"{i}", data.getattribute(i).url)
                )
            else:
                l.append(
                    (f"{i}", data.getattribute(i))
                )
    l.extend(kwargs.items())
    return dict(l)





def format_tarif(data):
    return OrderedDict([
        ('id', data.id),
        ('type', data.type),
        ('paket', data.paket),
        ("start_date", data.start_date),
        ("end_date", data.end_date),
        ("max_place", data.max_place),
        ("duration", data.duration),
        ("eating", data.eating),
        ("distance", data.distance),
        ("room", data.room),
        ("price_type", data.price_type),
        ("price", data.price),
        ("img", data.img.url),
    ])


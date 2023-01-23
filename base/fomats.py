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
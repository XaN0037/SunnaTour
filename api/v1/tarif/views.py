from collections import OrderedDict

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser


from api.v1.tarif.serializer import TarifSerializer

from base.helper import BearerAuth

from sayt.models import Tarif


def format(data):
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


class TarifViews(GenericAPIView):
    serializer_class = TarifSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BearerAuth,)
    parser_classes = (MultiPartParser,)

    def get(self, requests, pk=None, *args, **kwargs):

        if pk:
            try:
                result = format(Tarif.objects.get(pk=pk))
                return Response(result)
            except:
                result = {"ERROR": f"{pk} id bo'yicha hech qanday ma'lumot topilmadi"}
                return Response(result)

        else:
            result = []
            for i in Tarif.objects.all():
                result.append(format(i))

        return Response(result)

    def delete(self, requests, pk, *args, **kwargs):
        try:
            print('1')
            root = Tarif.objects.get(pk=pk)
            print(root)
            result = {"Succes": f"{root.paket} o'chirildi"}
            root.delete()

            return Response(result)
        except:
            return Response({"ERROR": "Bunday id mavjud emas"})

    def post(self, requests, *args, **kwargs):

        data = requests.data
        print(data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        root = serializer.create(serializer.data)

        return Response(format(root))

    def put(self, requests, pk, *args, **kwargs):

        data = requests.data
        new = Tarif.objects.get(pk=pk)
        serializer = self.get_serializer(data=data, instance=new, partial=True)
        serializer.is_valid(raise_exception=True)
        root = serializer.save()
        return Response(format(root))





Nodirbek
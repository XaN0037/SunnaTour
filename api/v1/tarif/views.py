from collections import OrderedDict

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser

from api.v1.tarif.serializer import TarifSerializer

from base.helper import BearerAuth

from sayt.models import Tarif


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


class TarifViews(GenericAPIView):
    serializer_class = TarifSerializer
    permission_classes = (AllowAny,)

    def get(self, requests, pk=None, *args, **kwargs):

        if pk:
            try:
                result = format_tarif(Tarif.objects.get(pk=pk))
                return Response(result)
            except:
                result = {"ERROR": f"{pk} id bo'yicha hech qanday ma'lumot topilmadi"}
                return Response(result)

        else:
            result = []
            for i in Tarif.objects.all():
                result.append(format_tarif(i))

        return Response(result)

    def delete(self, requests, pk, *args, **kwargs):
        try:

            root = Tarif.objects.get(pk=pk)

            result = {"Succes": f"{root.paket} o'chirildi"}
            root.delete()

            return Response(result)
        except:
            return Response({"ERROR": "Bunday id mavjud emas"})

    def post(self, requests, *args, **kwargs):

        serializer = self.get_serializer(data=requests.data)
        serializer.is_valid(raise_exception=True)
        root = serializer.save()

        return Response(format_tarif(root))

    def put(self, requests, pk, *args, **kwargs):
        print("asdfgh")

        print(requests)
        data = requests.data
        new = Tarif.objects.get(pk=pk)
        serializer = self.get_serializer(data=data, instance=new, partial=True)
        serializer.is_valid(raise_exception=True)
        root = serializer.save()
        return Response(format_tarif(root))

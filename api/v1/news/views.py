from collections import OrderedDict

from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from api.v1.news.serializer import NewsSerializer
from base.helper import BearerAuth
from sayt.models import News


def format(data):
    return OrderedDict([
        ('id', data.id),
        ('name', data.name),
        ('title', data.title),
        ('short_desc', data.short_desc),
        ('desc', data.desc),
        ('img', data.img.url),

    ])


class Newsview(GenericAPIView):
    serializer_class = NewsSerializer
    permission_classes = (AllowAny,)
    # authentication_classes = (BearerAuth,)
    parser_classes = (MultiPartParser,)

    def get(self, requests, pk=None, *args, **kwargs):

        if pk:
            try:
                result = format(News.objects.get(pk=pk))
                return Response(result)
            except:
                result = {"ERROR": f"{pk} id bo'yicha hech qanday ma'lumot topilmadi"}
                return Response(result)

        else:
            result = []
            for i in News.objects.all():
                result.append(format(i))

        return Response(result)

    def delete(self, requests, pk, *args, **kwargs):
        try:
            root = News.objects.get(pk=pk)
            result = {"Succes": f"{root.name} o'chirildi"}
            root.delete()
            return Response(result)
        except:
            return Response({"ERROR": "Bunday id mavjud emas"})

    def post(self, requests, *args, **kwargs):

        serializer = self.get_serializer(data=requests.data)
        serializer.is_valid(raise_exception=True)
        root = serializer.save()

        return Response(format(root))

    def put(self, requests, pk, *args, **kwargs):

        data = requests.data
        new = News.objects.get(pk=pk)
        serializer = self.get_serializer(data=data, instance=new, partial=True)
        serializer.is_valid(raise_exception=True)
        root = serializer.save()
        return Response(format(root))

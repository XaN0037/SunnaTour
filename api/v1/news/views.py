from collections import OrderedDict

from rest_framework.generics import GenericAPIView, ListCreateAPIView, UpdateAPIView, DestroyAPIView
# from rest_framework.parsers import MultiPartParser, FormParser
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


class Newsview(ListCreateAPIView, UpdateAPIView, DestroyAPIView):
    serializer_class = NewsSerializer
    permission_classes = (AllowAny,)
    # authentication_classes = (BearerAuth,)
    queryset = News



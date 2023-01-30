from collections import OrderedDict
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.models import User
from api.v1.tarif.serializer import TarifBronSerializer
from base.helper import BearerAuth
from sayt.models import TarifBron, Tarif


def format_bron(data):
    return OrderedDict([
        ('user', data.user.phone),
        ('tarif', data.tarif),
        ("status", data.status),
        ("create_date", data.create_at)
    ])


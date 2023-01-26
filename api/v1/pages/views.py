from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.v1.pages.pages import index, haj
from base.slavar import *

from api.v1.auth.serializer import Userserializer


class PagesView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        method = data.get('method')
        params = data.get('params')

        if not method:
            return Response({
                "Error": "method kiritilmagan"
            })

        if params is None:
            return Response({
                "Error": "params kiritilmagan"
            })

        if "lan" not in params:
            return Response({
                "Error": "params.lan kiritilmagan"
            })
        if params['lan'] not in ['uz', 'ru', "en"]:
            return Response({
                "Error": "Bunaqa til yo'q"
            })

        methods = ["index", 'haj']

        if method in methods:
            if method == "haj":
                result = haj(params['lan'])
            else:
                result = index(params['lan'])

            return Response({
                "page": method,
                "data": result,
            })
        else:
            return Response({
                "Error": "Method topilmadi"
            })

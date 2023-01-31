from collections import OrderedDict

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser

from api.v1.tarif.serializer import TarifSerializer, TarifBronSerializer
from api.v1.tarif.service import format_bron
from base.fomats import format_tarif

from base.helper import BearerAuth

from sayt.models import Tarif, TarifBron

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


# qo'shilgan joyi'

class ActionViews(GenericAPIView):
    serializer_class = TarifBronSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BearerAuth,)

    # parser_classes = (MultiPartParser,)

    def post(self, requests, *args, **kwargs):

        tipe = requests.data.get('method')
        paket = requests.data.get('params')

        if not tipe:
            return Response({
                "Error": "method kiritilmagan"
            })

        if paket is None or 'tarif_id' not in paket:
            return Response({
                "Error": "params to'lliq emas"
            })

        if tipe == 'bron':

            t = Tarif.objects.filter(pk=paket['tarif_id']).first()
            if not t:
                return Response({
                    "Error": "Bunaqa tarif topilmadi"
                })

            root = TarifBron()
            root.user = requests.user
            root.tarif = t
            root.save()
            return Response({'data': format_bron(root)})
        elif tipe == "change.pass":
            nott = "old" if "old" not in paket else "new" if "new" not in paket else None
            if nott:
                return Response({
                    "Error": f"params.{nott} polyasi to'ldirilmagan"

                })
            if not requests.user.check_password(paket['old']):
                return Response({
                    "Error": "Parol xato"
                })

            requests.user.set_password(paket['new'])
            requests.save()
            return Response({
                "Success": "Parol almashdi"
            })

        elif tipe == "del.bron":
            nott = "id" if "id" not in paket else None
            if nott:
                return Response({
                    "Error": f"params.{nott} polyasi to'ldirilmagan"

                })
            root = TarifBron.objects.filter(pk=paket['id']).first()
            if not root:
                return Response({
                    "Error": "Bron qilingan tarif topilmadi"
                })

            root.delete()
            return Response({
                "Success": "Bron qilingan tarif o'chirib tashlandi"
            })
        elif tipe == "all.brons":
            l = [format_bron(x) for x in TarifBron.objects.filter(user=requests.user)]
            return Response({
                "data": l
            })

        else:
            return Response({'Error': 'Bunday method mavjut emas'})

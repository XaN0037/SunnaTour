from rest_framework.views import APIView
from payme.models import Order, MerchatTransactionsModel
from rest_framework.response import Response
from rest_framework import status, permissions
import requests, json
from sayt.models import TarifBron
from payme.methods.generate_link import GeneratePayLink


class Payme(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        try:
            user = self.request.user
            params = self.request.query_params
            bron_id = params.get('bron_id')
            try:
                bron_id = int(bron_id)
                bron = TarifBron.objects.filter(id=bron_id, user=user.id).first()
            except Exception as e:
                return Response(
                    {
                        'status': False,
                        'error': 'Bron id not given or invalid id.'
                    }
                )
            cbu_uz_api = requests.get(url='https://cbu.uz/oz/arkhiv-kursov-valyut/json/')
            currency = json.loads(cbu_uz_api.content)[0]['Rate']
            if bron.tarif.price_type == 'UZS':
                amount = bron.tarif.price * 100
            else:
                amount = (bron.tarif.price * currency) * 100
            order = Order.objects.create(amount=amount)
            pay_link = GeneratePayLink(
                order_id=order.id,
                amount=amount
            ).generate_link()
        except Exception as e:
            return Response(
                {
                    "status": False,
                    "error": str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                "status": True,
                "data": {
                    'link': pay_link
                }
            }, status=status.HTTP_200_OK
        )

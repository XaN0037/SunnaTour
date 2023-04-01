from decimal import Decimal
import json
import requests
import base64
import binascii
from sayt.models import TarifBron
from django.conf import settings
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from api.v1.payment.payme.models import Order
from api.v1.payment.payme.utils.logger import logged
from api.v1.payment.payme.errors.exceptions import MethodNotFound
from api.v1.payment.payme.errors.exceptions import PermissionDenied
from api.v1.payment.payme.errors.exceptions import PerformTransactionDoesNotExist
from api.v1.payment.payme.methods.generate_link import GeneratePayLink
from api.v1.payment.payme.methods.check_transaction import CheckTransaction
from api.v1.payment.payme.methods.cancel_transaction import CancelTransaction
from api.v1.payment.payme.methods.create_transaction import CreateTransaction
from api.v1.payment.payme.methods.perform_transaction import PerformTransaction
from api.v1.payment.payme.methods.check_perform_transaction import CheckPerformTransaction


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
            currency = float(currency)
            amount = bron.tarif.price
            if not bron.tarif.price_type == 'UZS':
                amount = float(bron.tarif.price) * currency
            order = Order.objects.create(amount=int(amount), bron_id=bron_id)
            pay_link = GeneratePayLink(
                order_id=order.id,
                amount=Decimal(amount)
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

class MerchantAPIView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        password = request.META.get('HTTP_AUTHORIZATION')
        if self.authorize(password):
            incoming_data = request.data
            incoming_method = incoming_data.get("method")
            logged_message = "Incoming {data}"

            logged(
                logged_message=logged_message.format(
                    method=incoming_method,
                    data=incoming_data
                ),
                logged_type="info"
            )
            try:
                paycom_method = self.get_paycom_method_by_name(
                    incoming_method=incoming_method
                )
            except ValidationError:
                raise MethodNotFound()
            except PerformTransactionDoesNotExist:
                raise PerformTransactionDoesNotExist()

            paycom_method = paycom_method(incoming_data.get("params"))
            # headers = {
            #     "Content-Type": "application/json; charset=UTF-8",
            #     "Content-Length": 114,
            #     "Test-Operation": "Paycom",
            #     "Referer": "http://test.paycom.uz",
            #     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
            #     "Authorization": "Basic UGF5Y29tOng/JXJSYmNla1VHenJBVkB6QkhZTlVDQGo0cHFaa0pDRDZKJQ=="
            # }
        return Response(
            data=paycom_method,
            # headers=headers
        )

    @staticmethod
    def get_paycom_method_by_name(incoming_method: str) -> object:
        """
        Use this static method to get the paycom method by name.
        :param incoming_method: string -> incoming method name
        """
        available_methods: dict = {
            "CheckTransaction": CheckTransaction,
            "CreateTransaction": CreateTransaction,
            "CancelTransaction": CancelTransaction,
            "PerformTransaction": PerformTransaction,
            "CheckPerformTransaction": CheckPerformTransaction
        }

        try:
            MerchantMethod = available_methods[incoming_method]
        except Exception:
            error_message = "Unavailable method: %s" % incoming_method
            logged(
                logged_message=error_message,
                logged_type="error"
            )
            raise MethodNotFound(error_message=error_message)

        merchant_method = MerchantMethod()

        return merchant_method

    @staticmethod
    def authorize(password: str) -> None:
        """
        Authorize the Merchant.
        :param password: string -> Merchant authorization password
        """
        is_payme: bool = False
        error_message: str = ""

        if not isinstance(password, str):
            error_message = "Request from an unauthorized source!"
            logged(
                logged_message=error_message,
                logged_type="error"
            )
            raise PermissionDenied(error_message=error_message)

        password = password.split()[-1]
        try:
            password = base64.b64decode(password).decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            error_message = "Error when authorize request to merchant!"
            logged(
                logged_message=error_message,
                logged_type="error"
            )
            raise PermissionDenied(error_message=error_message)

        merchant_key = password.split(':')[-1]

        if merchant_key == settings.PAYME.get('PAYME_KEY'):
            is_payme = True

        if merchant_key != settings.PAYME.get('PAYME_KEY'):
            logged(
                logged_message="Invalid key in request!",
                logged_type="error"
            )

        if is_payme is False:
            raise PermissionDenied(
                error_message="Unavailable data for unauthorized users!"
            )

        return is_payme



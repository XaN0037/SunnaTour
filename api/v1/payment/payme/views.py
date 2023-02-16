from rest_framework import permissions
from rest_framework import status
from django.db import transaction
import json
import requests
from api.v1.pages.texts import Texts
from api.v1.payment.payme.responses import beautiful_response
from bmain.models import MonthlyPlan, PaymentCourseTransaction

import base64
import binascii
from django.conf import settings
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
    permission_classes = (permissions.IsAuthenticated,)

    def _validate_data(self):
        data = self.request.query_params
        lang = data.get('lang')
        monthly_payment = int(data.get('monthly_payment'))
        errors = []
        if not lang:
            errors.append(beautiful_response(lang=True))
        if not monthly_payment:
            errors.append(beautiful_response(monthly_payment=True))
        if lang and lang not in ['uz', 'ru', 'en']:
            errors.append(beautiful_response(lang_not_found=True))
        if monthly_payment:
            monthly_payment = MonthlyPlan.objects.select_related('minutes').filter(id=monthly_payment).first()
            if not monthly_payment:
                errors.append(beautiful_response(monthly_payment_not_found=True))
        return {
            "success": False,
            "message": "Error occurred",
            "error": errors,
            "data": []
        }

    def validate_order(self):
        data = self.request.query_params
        monthly_payment = int(data.get('monthly_payment'))
        lang = data.get('lang')
        cbu_uz_api = requests.get(url='https://cbu.uz/oz/arkhiv-kursov-valyut/json/')
        with transaction.atomic():
            amount = MonthlyPlan.objects.select_related('minutes').get(id=monthly_payment)
            currency = json.loads(cbu_uz_api.content)[0]['Rate']
            order_price = round((amount.monthly_price * float(currency) * 100) * float(amount.term_in_month), 2)
            create_order = Order.objects.create(amount=order_price)
            PaymentCourseTransaction.objects.create(
                user_id=self.request.user.id, order_id=create_order.id, monthly_plan_id=monthly_payment,
                dollar_currency=currency
            )
            return {
                "order_id": create_order.id,
                "amount": order_price,
                "monthly_payment": {
                    "month": f"{amount.term_in_month} {Texts['month'][lang]}",
                    "minutes": f"{amount.minutes.term} {Texts['buy_course']['minutes_lang'][lang]}",
                    "lesson": f"{amount.lesson} {Texts['lesson'][lang]}",
                    "price": round(amount.monthly_price * float(amount.term_in_month), 2),
                    "to_sum": round(order_price / 100, 2),
                    "discount": amount.discount,
                    "title": f'{Texts["buy_course"]["order_formalization"][lang]}',
                    "back": f'{Texts["buy_course"]["back"][lang]}',
                    "duration": f'{Texts["buy_course"]["duration"][lang]}',
                    "plan": f'{Texts["buy_course"]["plan"][lang]}',
                    "price_lang": f'{Texts["buy_course"]["price"][lang]}',
                    "pay_button": f'{Texts["buy_course"]["pay_button"][lang]}',
                }
            }

    def post(self, request):
        if self._validate_data().get('error'):
            return Response(self._validate_data(), status=status.HTTP_400_BAD_REQUEST)
        amount_and_order = self.validate_order()
        pay_link = GeneratePayLink(
            order_id=amount_and_order.get('order_id'),
            amount=amount_and_order.get('amount')
        ).generate_link()
        return Response(
            {
                "success": True,
                "message": "Link created successfully",
                "error": [],
                "data": {
                    'pay_link': pay_link,
                    'monthly_payment': amount_and_order.get('monthly_payment')
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

        return Response(data=paycom_method)

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



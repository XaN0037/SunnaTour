from api.v1.payment.payme.models import Order
from api.v1.payment.payme.utils.get_params import get_params
from api.v1.payment.payme.serializers import MerchatTransactionsModelSerializer


class CheckPerformTransaction:
    def __call__(self, params: dict) -> dict:
        data = get_params(params)
        serializer = MerchatTransactionsModelSerializer(
            data=data
        )
        serializer.is_valid(raise_exception=True)
        order = Order.objects.select_related('bron').filter(id=serializer.data.get('order_id')).first()
        response = {
            "result": {
                    "allow": True,
                }
                # 'detail': {
                #     'receipt_type': 0,
                #     'items': [
                #         {
                #             'title': order.bron.tarif.paket,
                #             'price': data.get('amount'),
                #             'cout': 1,
                #             'code': 10703999001000000, # Mhik,
                #             'package_code': 1495086, # Order id
                #             'vat_percent': 0
                #         }
                #     ]
                # }
            }

        return response

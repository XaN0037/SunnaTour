import time
from django.db import transaction

from api.v1.payment.payme.utils.get_params import get_params
from api.v1.payment.payme.models import MerchatTransactionsModel
from api.v1.payment.payme.serializers import MerchatTransactionsModelSerializer
from api.v1.payment.payme.errors.exceptions import PerformTransactionDoesNotExist


class CancelTransaction:

    @transaction.atomic
    def __call__(self, params: dict):
        serializer = MerchatTransactionsModelSerializer(
            data=get_params(params)
        )
        serializer.is_valid(raise_exception=True)
        clean_data = serializer.validated_data
        try:
            with transaction.atomic():
                transactions = MerchatTransactionsModel.objects.filter(_id=clean_data.get('_id'),).first()
                if transactions.cancel_time == 0:
                    transactions.cancel_time = int(time.time() * 1000)
                if transactions.perform_time == 0:
                    transactions.state = -1
                if transactions.perform_time != 0:
                    transactions.state = -2
                transactions.reason = clean_data.get("reason")
                transactions.save()

        except PerformTransactionDoesNotExist:
            raise PerformTransactionDoesNotExist()

        response: dict = {
            "result": {
                "state": transactions.state,
                "cancel_time": transactions.cancel_time,
                "transaction": transactions.transaction_id,
                "reason": int(transactions.reason),
            }
        }

        return response

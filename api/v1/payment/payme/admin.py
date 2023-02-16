from django.contrib import admin

from api.v1.payment.payme.models import Order
from api.v1.payment.payme.models import MerchatTransactionsModel

admin.site.register(Order)
admin.site.register(MerchatTransactionsModel)

from django.urls import path

from api.v1.payment.payme.views import MerchantAPIView


urlpatterns = [
    path("merchant/", MerchantAPIView.as_view())
]

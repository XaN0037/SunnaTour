from django.urls import path

from api.v1.auth.views import AuthView
from api.v1.tarif.views import Newsview

urlpatterns = [
        path("auth/", AuthView.as_view()),
        path("tarif/", Newsview.as_view()),
        path("tarif/<int:pk>/", Newsview.as_view()),
]
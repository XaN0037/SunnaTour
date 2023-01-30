from django.urls import path

from api.v1.auth.views import AuthView
from api.v1.news.views import Newsview
from api.v1.pages.views import PagesView
from api.v1.tarif.views import TarifViews, ActionViews

urlpatterns = [
    path("auth/", AuthView.as_view()),

    path("tarif/", TarifViews.as_view()),
    path("tarif/<int:pk>/", TarifViews.as_view()),

    path("new/<int:pk>/", Newsview.as_view(), name='api_new'),
    path("new/", Newsview.as_view(), name='api_new'),
    path("pages/", PagesView.as_view()),
    path('actions/', ActionViews.as_view())
]

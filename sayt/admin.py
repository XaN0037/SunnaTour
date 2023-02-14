from django.contrib import admin

from api.models import ServerTokens
from sayt.models import News, Tarif, TarifBron

# Register your models here.



admin.site.register(News)


admin.site.register(Tarif)
admin.site.register(ServerTokens)
admin.site.register(TarifBron)

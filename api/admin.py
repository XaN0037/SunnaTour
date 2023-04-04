from django.contrib import admin

from api.models import ServerTokens, User

# Register your models here.


admin.register(ServerTokens)
admin.site.register(User)

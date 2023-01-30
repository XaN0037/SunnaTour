from rest_framework import serializers

from sayt.models import Tarif, TarifBron


class TarifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarif
        fields = '__all__'


# qo'shilgan joyi

class TarifBronSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarifBron
        fields = '__all__'

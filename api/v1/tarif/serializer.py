from rest_framework import serializers

from sayt.models import Tarif


class TarifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarif
        fields = '__all__'

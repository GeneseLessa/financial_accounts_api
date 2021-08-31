from rest_framework import serializers
from .models import FinancialAccount


class FinancialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialAccount
        fields = '__all__'

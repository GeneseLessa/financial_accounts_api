from rest_framework.serializers import ModelSerializer
from .models import Sender


class SenderSerializer(ModelSerializer):
    class Meta:
        model = Sender
        fields = '__all__'

from .models import agent_model, AiModel
from rest_framework import serializers


class AgentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = agent_model
        fields = '__all__'

class AiModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AiModel
        fields = '__all__'
        
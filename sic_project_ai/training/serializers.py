from .models import agent_model
from rest_framework import serializers


class AgentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = agent_model
        fields = '__all__'
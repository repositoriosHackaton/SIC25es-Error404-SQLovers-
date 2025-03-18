from .models import MLExperiment, FeatureImportance, Prediction
from rest_framework import serializers

class MlExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLExperiment
        fields = '__all__'
        
class FeatureImportanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureImportance
        fields = '__all__'
        
class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'  
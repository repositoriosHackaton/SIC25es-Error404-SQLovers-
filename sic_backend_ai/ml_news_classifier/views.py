from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg import openapi
from .models import MLExperiment, FeatureImportance, Prediction
from .serializers import MlExperimentSerializer, FeatureImportanceSerializer, PredictionSerializer
from rest_framework import viewsets

# Create your views here.

class MlExperimentsView(viewsets.ModelViewSet):
    queryset = MLExperiment.objects.all()
    serializer_class = MlExperimentSerializer

class FeatureImportanceView(viewsets.ModelViewSet):
    queryset = FeatureImportance.objects.all()
    serializer_class = FeatureImportanceSerializer
    
class PredictionView(viewsets.ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
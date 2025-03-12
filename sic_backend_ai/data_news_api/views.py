from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import NewsDataset, Article, Feature, MLModel
from .serializers import NewsDatasetSerializer, ArticleSerializer, FeatureSerializer, MLModelSerializer
from .docs import NewsDatasetDocsVIEWSET, ArticleDocsVIEWSET, FeaturesDocsVIEWSET, MLModelsDocsVIEWSET
# Create your views here.

class NewsDatasetView(NewsDatasetDocsVIEWSET):
    queryset = NewsDataset.objects.all()
    serializer_class = NewsDatasetSerializer

class ArticleView(ArticleDocsVIEWSET):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class FeatureView(FeaturesDocsVIEWSET):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

class MLModelView(MLModelsDocsVIEWSET):
    queryset = MLModel.objects.all()
    serializer_class = MLModelSerializer


class MigratedDatasetStats(APIView):
    @swagger_auto_schema(
        operation_description="Get the number of records in each table",
        responses={200: openapi.Response('Success', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'news_dataset': openapi.Schema(type=openapi.TYPE_INTEGER),
                'articles': openapi.Schema(type=openapi.TYPE_INTEGER),
                'features': openapi.Schema(type=openapi.TYPE_INTEGER),
                'ml_models': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        ))},
        tags=['Dataset Stats to use in Machine Learning Operations - MLO']
    )
    def get(self, request):
        news_dataset = NewsDataset.objects.all()
        articles = Article.objects.all()
        features = Feature.objects.all()
        ml_models = MLModel.objects.all()
        
        return Response({
            'news_dataset': news_dataset.count(),
            'articles': articles.count(),
            'features': features.count(),
            'ml_models': ml_models.count()
        })
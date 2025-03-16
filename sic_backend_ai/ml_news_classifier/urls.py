from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MlExperimentsView, FeatureImportanceView, PredictionView

router = DefaultRouter()
router.register(r'ml_news_classifier/ml-experiments/api/v1/data', MlExperimentsView, basename='ml-experiment')
router.register(r'ml_news_classifier/feature-importance/api/v1/data', FeatureImportanceView, basename='feature-importance')
router.register(r'ml_news_classifier/predictions/api/v1/data', PredictionView, basename='prediction')

urlpatterns = [
    path('', include(router.urls)),
]

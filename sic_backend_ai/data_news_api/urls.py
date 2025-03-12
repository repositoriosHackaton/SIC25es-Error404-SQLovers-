from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsDatasetView, ArticleView, FeatureView, MLModelView, MigratedDatasetStats

router = DefaultRouter()
router.register(r'data_news/news-dataset/api/v1/data', NewsDatasetView, basename='news-dataset')
router.register(r'data_news/articles/api/v1/data', ArticleView, basename='article')
router.register(r'data_news/features/api/v1/data', FeatureView, basename='feature')
router.register(r'data_news/ml-models/api/v1/data', MLModelView, basename='ml-model')



urlpatterns = [
    path('', include(router.urls)),
    path('dataset-stats/', MigratedDatasetStats.as_view(), name='dataset-stats'),
]

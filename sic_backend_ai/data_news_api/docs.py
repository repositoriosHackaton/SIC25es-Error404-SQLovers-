from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets
from .models import NewsDataset, Article, Feature, MLModel
from .serializers import NewsDatasetSerializer, ArticleSerializer, FeatureSerializer, MLModelSerializer

class BaseDocumentedViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet with documentation for common CRUD operations.
    """
    @swagger_auto_schema(
        operation_summary="Retrieve an entry",
        operation_description="Returns an entry by ID",
        tags=['API'],
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the entry", type=openapi.TYPE_INTEGER)
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete an entry",
        operation_description="Deletes an entry by ID",
        tags=['API'],
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the entry", type=openapi.TYPE_INTEGER)
        ]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class NewsDatasetDocsVIEWSET(BaseDocumentedViewSet):
    """
    API endpoints for managing news dataset entries.
    """
    queryset = NewsDataset.objects.all()
    serializer_class = NewsDatasetSerializer

    # Aplica un esquema automático a todos los métodos (para evitar repetir código)
    @swagger_auto_schema(
        operation_summary="List all news dataset entries",
        operation_description="Returns a list of all news dataset entries",
        tags=['Datasets API']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a news dataset entry",
        operation_description="Creates a new news dataset entry with state and article data",
        tags=['Datasets API'],
        request_body=NewsDatasetSerializer  # Especifica el request body
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a news dataset entry",
        operation_description="Returns a single news dataset entry by ID",
        tags=['Datasets API'],
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the entry", type=openapi.TYPE_INTEGER)
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a news dataset entry",
        operation_description="Updates an existing news dataset entry by ID",
        tags=['Datasets API'],
        request_body=NewsDatasetSerializer
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update for news dataset entry",
        operation_description="Partially updates an existing news dataset entry by ID",
        tags=['Datasets API'],
        request_body=NewsDatasetSerializer
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a news dataset entry",
        operation_description="Deletes a news dataset entry by ID",
        tags=['Datasets API'],
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the entry", type=openapi.TYPE_INTEGER)
        ]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ArticleDocsVIEWSET(BaseDocumentedViewSet):
    """
    Documentation for Articles API
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    @swagger_auto_schema(
        operation_summary="List all articles",
        operation_description="Returns a list of all articles",
        tags=['Articles API']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create an article",
        operation_description="Creates a new article with text and label data",
        tags=['Articles API'],
        request_body=ArticleSerializer
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve an article",
        operation_description="Returns a single article by ID",
        tags=['Articles API'],
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the entry", type=openapi.TYPE_INTEGER)
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update an article",
        operation_description="Updates an existing article by ID",
        tags=['Articles API'],
        request_body=ArticleSerializer
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update for an article",
        operation_description="Partially updates an existing article by ID",
        tags=['Articles API'],
        request_body=ArticleSerializer
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete an article",
        operation_description="Deletes an article by ID",
        tags=['Articles API'],
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the entry", type=openapi.TYPE_INTEGER)
        ]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    

class FeaturesDocsVIEWSET(BaseDocumentedViewSet):
    """
    Documentation for Features API
    """
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

    @swagger_auto_schema(
        operation_summary="List all features",
        operation_description="Returns a list of all features",
        tags=['Features API']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a feature",
        operation_description="Creates a new feature with name and value data",
        tags=['Features API'],
        request_body=FeatureSerializer
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a feature",
        operation_description="Returns a single feature by ID",
        tags=['Features API'],
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the entry", type=openapi.TYPE_INTEGER)
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a feature",
        operation_description="Updates an existing feature by ID",
        tags=['Features API'],
        request_body=FeatureSerializer
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update for a feature",
        operation_description="Partially updates an existing feature by ID",
        tags=['Features API'],
        request_body=FeatureSerializer
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a feature",
        operation_description="Deletes a feature by ID",
        tags=['Features API'],
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the entry", type=openapi.TYPE_INTEGER)
        ]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class MLModelsDocsVIEWSET(BaseDocumentedViewSet):
    """
    Documentation for ML Models API
    """
    queryset = MLModel.objects.all()
    serializer_class = MLModelSerializer

    @swagger_auto_schema(
        operation_summary="List all ML models",
        operation_description="Returns a list of all ML models",
        tags=['ML Models API']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create an ML model",
        operation_description="Creates a new ML model with name and description data",
        tags=['ML Models API'],
        request_body=MLModelSerializer
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve an ML model",
        operation_description="Returns a single ML model by ID",
        tags=['ML Models API'],
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the entry", type=openapi.TYPE_INTEGER)
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update an ML model",
        operation_description="Updates an existing ML model by ID",
        tags=['ML Models API'],
        request_body=MLModelSerializer
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update for an ML model",
        operation_description="Partially updates an existing ML model by ID",
        tags=['ML Models API'],
        request_body=MLModelSerializer
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete an ML model",
        operation_description="Deletes an ML model by ID",
        tags=['ML Models API'],
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the entry", type=openapi.TYPE_INTEGER)
        ]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
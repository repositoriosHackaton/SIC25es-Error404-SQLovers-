from rest_framework import serializers
from .models import NewsDataset, Article, Feature, MLModel

class NewsDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsDataset
        fields = '__all__'
    
    def __str__(self):
        return self.state

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
    
    def __str__(self):
        return self.text

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'
    
    def __str__(self):
        return self.feature_name

class MLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = '__all__'
    
    def __str__(self):
        return self.name
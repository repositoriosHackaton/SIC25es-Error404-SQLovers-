from django.db import models
from django.utils import timezone
from data_news_api.models import Article, MLModel

class MLExperiment(models.Model):
    """Track machine learning experiments"""
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    algorithm_name = models.CharField(max_length=100)
    parameters = models.JSONField(default=dict)
    
    accuracy = models.FloatField(null=True, blank=True)
    precision = models.FloatField(null=True, blank=True)
    recall = models.FloatField(null=True, blank=True)
    f1_score = models.FloatField(null=True, blank=True)
    
    ml_model = models.ForeignKey(MLModel, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.algorithm_name})"


class FeatureImportance(models.Model):
    """Store feature importance from trained models"""
    experiment = models.ForeignKey(MLExperiment, on_delete=models.CASCADE, related_name='feature_importances')
    feature_name = models.CharField(max_length=200)
    importance = models.FloatField()
    
    class Meta:
        unique_together = ('experiment', 'feature_name')
        
    def __str__(self):
        return f"{self.feature_name}: {self.importance}"


class Prediction(models.Model):
    """Store model predictions for new articles"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='ml_predictions')
    experiment = models.ForeignKey(MLExperiment, on_delete=models.CASCADE)
    prediction = models.CharField(max_length=10, choices=Article.LABEL_CHOICES)
    confidence = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Prediction for article {self.article_id}: {self.prediction} ({self.confidence:.2f})"
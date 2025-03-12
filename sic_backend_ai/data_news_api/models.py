from django.db import models
from django.utils import timezone

# Create your models here.

class NewsDataset(models.Model):
    
    state = models.CharField(max_length=100, null=True)
    article = models.TextField(null=True)

class Article(models.Model):
    """Main model to store news articles and their classification status"""
    
    # Classification status
    TRUE = 'true'
    FALSE = 'false'
    UNKNOWN = 'unknown'
    
    LABEL_CHOICES = [
        (TRUE, 'True'),
        (FALSE, 'False'),
        (UNKNOWN, 'Unknown'),
    ]
    
    # Basic article data
    text = models.TextField()
    label = models.CharField(max_length=10, choices=LABEL_CHOICES, default=UNKNOWN)
    title = models.TextField(null=True, blank=True)
    
    # Metadata
    source = models.CharField(max_length=255, null=True, blank=True)
    dataset_origin = models.CharField(max_length=100, null=True, blank=True)  # Which dataset it came from
    language = models.CharField(max_length=10, default='es')
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # ML specific fields
    in_training_set = models.BooleanField(default=False)
    in_test_set = models.BooleanField(default=False)
    
    # Optional fields for prediction results
    prediction = models.CharField(max_length=10, choices=LABEL_CHOICES, null=True, blank=True)
    prediction_confidence = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        """Return a string representation of the article"""
        return f"{self.text[:50]}... ({self.label})"


class Feature(models.Model):
    """Store extracted features from articles for ML training"""
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='features')
    feature_name = models.CharField(max_length=100)
    feature_value = models.FloatField()
    
    class Meta:
        unique_together = ('article', 'feature_name')
        
    def __str__(self):
        return f"{self.feature_name}: {self.feature_value}"


class MLModel(models.Model):
    """Store information about trained ML models"""
    
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    # Model performance metrics
    accuracy = models.FloatField(null=True, blank=True)
    precision = models.FloatField(null=True, blank=True)
    recall = models.FloatField(null=True, blank=True)
    f1_score = models.FloatField(null=True, blank=True)
    
    # Model binary data could be stored here or in a file field
    model_file = models.FileField(upload_to='ml_models/', null=True, blank=True)
    
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
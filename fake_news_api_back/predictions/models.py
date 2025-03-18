from django.db import models

class Prediction(models.Model):
    text = models.TextField()
    prediction = models.CharField(max_length=10, choices=[("Real", "Real"), ("Fake", "Fake")])
    model_used = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prediction} ({self.model_used})"

class TrainingStats(models.Model):
    model_name = models.CharField(max_length=50)
    accuracy = models.FloatField()
    trained_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model_name} - {self.accuracy:.2f}"

from django.db import models

# Create your models here.
class agent_model(models.Model):
    agent_name = models.CharField(max_length=50)
    agent_type = models.CharField(max_length=50)
    agent_description = models.CharField(max_length=50)
    agent_status = models.CharField(max_length=50)
    agent_created = models.DateTimeField(auto_now_add=True)
    agent_updated = models.DateTimeField(auto_now=True)
    agent_lore = models.TextField(max_length=max)
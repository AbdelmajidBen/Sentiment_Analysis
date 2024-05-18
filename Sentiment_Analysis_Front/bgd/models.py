from django.db import models
from django.contrib.postgres.fields import ArrayField

class Tweet(models.Model):
    timestamp = models.DateTimeField()
    prediction = models.CharField(max_length=100)
    TweetContent = models.CharField(max_length=500, default="None")
    rawPredictionArray = ArrayField(models.FloatField(), default=list)
    cpu_usage = models.FloatField(default=-1)  # Add cpu_usage field
    memory_usage = models.FloatField(default=-1)  # Add memory_usage field

    class Meta:
        db_table = 'tweets'  # MongoDB collection name


from django.db import models
from django.contrib.postgres.fields import ArrayField 
 
class Tweet(models.Model):
    timestamp = models.DateTimeField()
    prediction = models.CharField(max_length=100)
    TweetContent = models.CharField(max_length=500 , default="None")
    rawPredictionArray = ArrayField(models.FloatField(), default=[])  # Assuming rawPrediction is an array of floats  # Assuming rawPredictionArray is a JSONField
    class Meta:
        db_table = 'tweets'  # MongoDB collection name


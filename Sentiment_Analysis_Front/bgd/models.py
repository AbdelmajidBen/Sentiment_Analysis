
from django.db import models

class Tweet(models.Model):
    ID = models.CharField(max_length=50)
    company = models.CharField(max_length=100)
    Sentiment = models.CharField(max_length=50)
    tweet = models.TextField()

    class Meta:
        db_table = 'tweets'  # MongoDB collection name

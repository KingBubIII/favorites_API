from django.db import models

class Favorites(models.Model):
    name = models.CharField(max_length=250, null=False)
    rank = models.IntegerField(null=False)
    comments = models.CharField(max_length=250)
    link = models.CharField(max_length=100)
    category = models.CharField(max_length=50, null=False)
    added_by_suggestion =models.BooleanField(null=False)

class Suggestions(models.Model):
    name = models.CharField(max_length=100, null=False)
    comments = models.CharField(max_length=250)
    link = models.CharField(max_length=100)
    category = models.CharField(max_length=50, null=False)
    suggester = models.CharField(max_length=100)
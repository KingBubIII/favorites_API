from django.db import models


class Favorites(models.Model):
    class Meta:
        db_table = "favorites"

    name = models.CharField(max_length=100)
    rank = models.IntegerField()
    comments = models.CharField(max_length=250, blank=True, null=True)
    link = models.URLField(blank=True, null=True, unique=True)
    category = models.CharField(max_length=50)
    added_by_suggestion = models.BooleanField(default=0)
    date_added = models.DateField(auto_now_add=True)


class Suggestions(models.Model):
    class Meta:
        db_table = "suggestions"

    name = models.CharField(max_length=100)
    comments = models.CharField(max_length=250, blank=True, null=True)
    link = models.CharField(blank=True, null=True, unique=True)
    category = models.CharField(max_length=50)
    suggester = models.CharField(max_length=50, blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)

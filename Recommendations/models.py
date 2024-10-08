from django.db import models


class Recommendations(models.Model):
    class Meta:
        db_table = "recommendations"

    name = models.CharField(max_length=100)
    comments = models.CharField(max_length=250, blank=True, null=True)
    link = models.URLField(blank=True, null=True, unique=True)
    category = models.CharField(max_length=50)
    suggester = models.CharField(max_length=50, blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)

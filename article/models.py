from django.db import models


class Article(models.Model):
    """
    Articles!
    """
    title = models.CharField(max_length=255)

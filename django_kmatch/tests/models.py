from django.db import models

from django_kmatch import KField


class KModel(models.Model):
    """
    A model for testing saving and compiling of K objects.
    """
    k = KField()


class NullTrueModel(models.Model):
    """
    A model with a null=True KField.
    """
    k = KField(null=True)

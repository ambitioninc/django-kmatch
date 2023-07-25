from django.db import models

from django_kmatch import KField


class KModel(models.Model):
    """
    A model for testing saving and compiling of K objects.
    """
    k = KField(null=False)


class NullTrueModel(models.Model):
    """
    A model with a null=True KField.
    """
    k = KField(null=True)
    knone = KField(null=True, default=None)


class KDefModel(models.Model):
    """
    A model for testing saving and compiling of K objects.
    """
    kdict = KField(null=False, default=dict)
    klist = KField(null=False, default=list)

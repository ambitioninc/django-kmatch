from django.db import models

from django_kmatch import KField, KField2


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


class KModel2(models.Model):
    """
    A model for testing saving and compiling of K objects.
    """
    k = KField2()


class NullTrueModel2(models.Model):
    """
    A model with a null=True KField.
    """
    k = KField2(null=True)

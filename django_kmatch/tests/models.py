from django.db import models

from django_kmatch import KField


class KModel(models.Model):
    """
    A model for testing saving and compiling of K objects.
    """
    # Very oddly, the legacy jsonfield works differently whether default=None is specified or not.
    # With default=None, you can create an object with a k field and it gets a json-null value.
    # Without the default=None (and null=False is specified or defaulted), something happens and
    # the K object itself gets an empty value and complains that it is not a valid pattern.

    # This is neither here nor there I guess, as we have moved on from the legacy jsonfield, and
    # this specific behavior does not seem like something useful that needs to be duplicated. Going forward,
    # essentially the default=None is implied.
    k = KField(default=None)


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

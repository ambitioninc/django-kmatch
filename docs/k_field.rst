KField custom model field
=========================

The django-kmatch app comes with a ``KField`` custom model field that can be used to store kmatch patterns and obtain associated ``K`` objects. An example of using the field in a model definition is below:

.. code-block:: python

    from django.db import models
    from django_kmatch import KField

    class KModel(models.Model):
        k = KField()

Using the ``KField`` is done like the following:

.. code-block:: python

    # Create a KModel object with a pattern to match dictionaries with a 'a' field of 2
    k_model = KModel.objects.create(k=['==', 'a', 2])

    # Match dictionaries with the K object returned from the KField
    print k_model.k.match({'a': 2})
    True

The ``KField`` field also does validation of the pattern:

.. code-block:: python

    # Create a KModel with an invalid pattern
    k_model = KModel.objects.create(k='invalid')
    Traceback (most recent call last):
        # Traceback message here ...
    ValueError: Not a valid operator or filter - 'invalid'

Nullable ``KField`` values are fine as well.
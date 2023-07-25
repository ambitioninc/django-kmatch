import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import JSONField as DjangoJSONField
from ambition_utils.fields import CastOnAssignFieldMixin
from kmatch import K


class KField(CastOnAssignFieldMixin, DjangoJSONField):
    """Stores a kmatch pattern and returns a compiled K object.

        The KField field stores a kmatch pattern in a JSONField. The pattern is compiled and returned as
        a K object when accessing the field. Invalid kmatch patterns cannot be stored.
        """
    description = 'A kmatch pattern'

    def __init__(self, *args, **kwargs):
        self.dump_kwargs = kwargs.pop('dump_kwargs', {
            'cls': DjangoJSONEncoder,
            'separators': (',', ':')
        })
        self.load_kwargs = kwargs.pop('load_kwargs', {})

        super().__init__(*args, **kwargs)

    # This method is overridden in JSONField in Django 4.2 but not in 4.1. In 4.2 it completely bypasses
    # get_db_prep_value() if the value is None, preventing the possibility of storing a "json null"
    # in a not-null field. So we are forcing it here to be its original (pre-4.2) self so we can decide
    # for ourselves how to handle a None.
    def get_db_prep_save(self, value, connection):
        return self.get_db_prep_value(value, connection, prepared=False)

    def get_db_prep_value(self, value, connection, prepared=False):
        """
        Converts a K object to a pattern.
        """
        # If we have a K object, what we save into the database is the pattern.
        if isinstance(value, K):
            value = value.pattern

        # If the field IS NULLABLE and we pass in a None, then we return a None which will get stored
        # as a real database NULL value. Note that we are directly returning the value, NOT passing it
        # through super().get_db_prep_value, which SPECIFICALLY IN DJANGO 4.2+
        # would have the effect of setting the json null value.
        if self.null and value is None:
            return None

        # If we have a None value in a non-nullable field, we save the json equivalent of null, i.e. "null"
        # But once again, we do NOT want to pass it through the super().db_prep_value or it will try to
        # double-wrap, literally '"null"'
        if not self.null and value is None:
            return json.dumps(value)

        return super().get_db_prep_value(value, connection, prepared=False)

    def to_python(self, value):
        """
        Used to obtain a K object for a provided pattern.
        """
        if isinstance(value, K) or value is None:
            return value

        if isinstance(value, str):
            # We really should not ever get here - the only way would be if the json
            # was invalid, in which case we'll end up with a value error anyway.
            return K(json.loads(value))
        else:
            return K(value)

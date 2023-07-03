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

    def get_db_prep_value(self, value, connection, prepared=False):
        """
        Converts a K object to a pattern.
        """
        if isinstance(value, K):
            value = value.pattern

        if not self.null and value is None:
            value = json.dumps(value)

        return super(KField, self).get_db_prep_value(value, connection, prepared=False)

    def to_python(self, value):
        """
        Used to obtain a K object for a provided pattern.
        """
        if not isinstance(value, K) and value is not None:
            if isinstance(value, str):
                return json.loads(value)
            else:
                return K(value)
        return value

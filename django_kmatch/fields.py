import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import JSONField as DjangoJSONField
from jsonfield import JSONField
from jsonfield.subclassing import Creator
from kmatch import K


class KField(JSONField):
    """Stores a kmatch pattern and returns a compiled K object.

    The KField field stores a kmatch pattern in a JSONField. The pattern is compiled and returned as
    a K object when accessing the field. Invalid kmatch patterns cannot be stored.
    """
    description = 'A kmatch pattern'

    def pre_init(self, value, obj):
        """
        Used to obtain a K object for a provided pattern. Normally this is done in the to_python method
        of a Django custom field. However, this field inherits JSONField, and JSONField had to do
        conversions in the pre_init method.
        """
        value = super(KField, self).pre_init(value, obj)
        return K(value) if not isinstance(value, K) and value is not None else value

    def get_db_prep_value(self, value, connection, prepared=False):
        """
        Converts a K object to a pattern.
        """
        if isinstance(value, K):
            value = value.pattern
        return super(KField, self).get_db_prep_value(value, connection, prepared=False)


class KField2(DjangoJSONField):
    """Stores a kmatch pattern and returns a compiled K object.

        The KField2 field stores a kmatch pattern in a JSONField. The pattern is compiled and returned as
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
        return super(KField2, self).get_db_prep_value(value, connection, prepared=False)

    def pre_init(self, value, obj):
        """
        Used to obtain a K object for a provided pattern. Normally this is done in the to_python method
        of a Django custom field. However, this field inherits JSONField, and JSONField had to do
        conversions in the pre_init method.
        """
        return K(value) if not isinstance(value, K) and value is not None else value

    def contribute_to_class(self, cls, name, private_only=False):
        super().contribute_to_class(cls, name)
        setattr(cls, name, Creator(self))

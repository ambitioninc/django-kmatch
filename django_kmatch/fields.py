from jsonfield import JSONField
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
        Converts a K object to a pattern. This pattern will be serialized to JSON and saved as a
        TextField.
        """
        if isinstance(value, K):
            value = value.pattern
        return super(KField, self).get_db_prep_value(value, connection, prepared=False)

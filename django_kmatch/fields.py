from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import JSONField as DjangoJSONField
from jsonfield import JSONField
# from jsonfield.subclassing import Creator
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

# This was lifted from jsonfield/subclassing.py

class Creator(object):
    """
    A placeholder class that provides a way to set the attribute on the model.
    """
    def __init__(self, field):
        print('hello from Creator.__init__!')
        self.field = field

    def __get__(self, obj, type=None):
        print('hello from Creator.__get__!')
        if obj is None:
            raise AttributeError('Can only be accessed via an instance.')
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        print('hello from Creator.__set__!')
        # Usually this would call to_python, but we've changed it to pre_init
        # so that we can tell which state we're in. By passing an obj,
        # we can definitively tell if a value has already been deserialized
        # More: https://github.com/bradjasper/django-jsonfield/issues/33
        obj.__dict__[self.field.name] = self.field.pre_init(value, obj)


class KField2(DjangoJSONField):
    """Stores a kmatch pattern and returns a compiled K object.

        The KField2 field stores a kmatch pattern in a JSONField. The pattern is compiled and returned as
        a K object when accessing the field. Invalid kmatch patterns cannot be stored.
        """
    description = 'A kmatch pattern'

    def __init__(self, *args, **kwargs):
        print('hello from KField2.__init__!')
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
        print('hello from KField2.get_db_prep_value!')
        if isinstance(value, K):
            value = value.pattern
        return super(KField2, self).get_db_prep_value(value, connection, prepared=False)

    def pre_init(self, value, obj):
        """
        Used to obtain a K object for a provided pattern. Normally this is done in the to_python method
        of a Django custom field. However, this field inherits JSONField, and JSONField had to do
        conversions in the pre_init method.
        """
        print('hello from KField2.pre_init!')
        return K(value) if not isinstance(value, K) and value is not None else value

    def contribute_to_class(self, cls, name, private_only=False):
        print('hello from KField2.contribute_to_class!')
        super().contribute_to_class(cls, name)
        setattr(cls, name, Creator(self))

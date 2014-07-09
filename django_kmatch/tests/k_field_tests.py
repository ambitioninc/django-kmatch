from mock import patch

from django.test import TestCase
from kmatch import K

from .models import KModel, NullTrueModel


class RegexFieldTest(TestCase):
    """
    Tests storing and calling functions/classes that are stored in test models.
    """
    @patch('south.modelsinspector.add_introspection_rules', spec_set=True)
    def test_without_south(self, mock_add_introspection_rules):
        """
        Tests that the k field still works fine without south installed.
        """
        # Create a mock function that raises an ImportError when souths modelsinspector is
        # imported
        orig_import = __import__

        def import_mock(name, *args):
            if name == 'south.modelsinspector':
                raise ImportError
            return orig_import(name, *args)

        # Reload the field where we do south-specific stuff. Do this while raising an
        # import error for south. Verify that add_introspection_rules isn't called
        with patch('__builtin__.__import__', side_effect=import_mock):
            from django_kmatch import fields
            reload(fields)

        self.assertFalse(mock_add_introspection_rules.called)

    def test_null(self):
        """
        Tests that null k patterns can be saved with null=True.
        """
        test_obj = NullTrueModel.objects.create(k=None)
        self.assertEquals(test_obj.k, None)
        test_obj = NullTrueModel.objects.get(id=test_obj.id)
        self.assertEquals(test_obj.k, None)

    def test_save_list(self):
        """
        Tests that k lists are saved and accessed properly.
        """
        test_obj = KModel.objects.create(k=['==', 'a', 1])
        self.assertTrue(test_obj.k.match({'a': 1}))
        self.assertFalse(test_obj.k.match({'a': 2}))

        # Set the value of the test obj and call save. Verify the k object can still be loaded properly
        test_obj.k = ['==', 'z', 2]
        test_obj.save()
        test_obj = KModel.objects.get(id=test_obj.id)
        self.assertTrue(test_obj.k.match({'z': 2}))
        self.assertFalse(test_obj.k.match({'z': 3}))

    def test_save_k(self):
        """
        Tests that compiled k patterns can be saved and accessed.
        """
        k = K(['==', 'a', 1])
        test_obj = KModel.objects.create(k=k)
        self.assertTrue(test_obj.k.match({'a': 1}))
        self.assertFalse(test_obj.k.match({'a': 2}))

        # Set the value of the test obj and call save. Verify the function can still be loaded properly
        test_obj.k = K(['==', 'z', 2])
        test_obj.save()
        test_obj = KModel.objects.get(id=test_obj.id)
        self.assertTrue(test_obj.k.match({'z': 2}))
        self.assertFalse(test_obj.k.match({'z': 3}))

    def test_invalid_pattern(self):
        """
        Tests accessing an invalid kmatch pattern.
        """
        with self.assertRaises(ValueError):
            KModel.objects.create(k='he(lo')

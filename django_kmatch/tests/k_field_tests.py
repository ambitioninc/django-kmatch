from django.test import TestCase
from kmatch import K

from .models import KModel, NullTrueModel


class KFieldTest(TestCase):
    """
    Tests storing and calling functions/classes that are stored in test models.
    """
    def test_null(self):
        """
        Tests that null k patterns can be saved with null=True.
        """
        test_obj = NullTrueModel.objects.create(k=None)
        self.assertEqual(test_obj.k, None)
        test_obj = NullTrueModel.objects.get(id=test_obj.id)
        self.assertEqual(test_obj.k, None)

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

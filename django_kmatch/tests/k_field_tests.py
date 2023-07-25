import json
from django.db import IntegrityError
from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import connection, models
from kmatch import K
from django.db.models import Value, JSONField
from django_kmatch import KField
from .models import KModel, NullTrueModel

def get_field_value(model='kmodel', field='k'):
    sqlcmd = f'select {field} from tests_{model} order by id desc'
    with connection.cursor() as cursor:
        cursor.execute(sqlcmd)
        row = cursor.fetchone()
        return row[0]

class KFieldTest(TestCase):
    """
    Tests storing and calling functions/classes that are stored in test models.
    """
    def test_save_list(self):
        """
        Tests that k lists are saved and accessed properly when a list constructor is passed in.
        """
        test_obj = KModel.objects.create(k=['==', 'a', 1])
        self.assertTrue(test_obj.k.match({'a': 1}))
        self.assertFalse(test_obj.k.match({'a': 2}))

        # Prove that the k field in the object returned from the create is a real K object.
        self.assertTrue(isinstance(test_obj.k, K))

        # Set the value of the test obj and call save. Verify the k object can still be loaded properly
        test_obj.k = ['==', 'z', 2]
        test_obj.save()
        test_obj = KModel.objects.get(id=test_obj.id)
        self.assertTrue(test_obj.k.match({'z': 2}))
        self.assertFalse(test_obj.k.match({'z': 3}))

        # Once again, make sure we have a K object.
        self.assertTrue(isinstance(test_obj.k, K))

        # Verify that the type stored in the database is a json value that comes out as a string when
        # queried directly.
        dbval = get_field_value('kmodel', 'k')
        # When reading the value directly via sql, we should see a string. It should load into a list.
        self.assertEqual(type(dbval), str)
        self.assertEqual(type(json.loads(dbval)), list)


    def test_save_k(self):
        """
        Tests that compiled k patterns can be saved and accessed.
        """
        k = K(['==', 'a', 1])
        test_obj = KModel.objects.create(k=k)
        self.assertTrue(test_obj.k.match({'a': 1}))
        self.assertFalse(test_obj.k.match({'a': 2}))

        # Prove that the k field in the object returned from the create is a real K object.
        self.assertTrue(isinstance(test_obj.k, K))

        # Set the value of the test obj and call save. Verify the function can still be loaded properly
        test_obj.k = K(['==', 'z', 2])
        test_obj.save()
        test_obj = KModel.objects.get(id=test_obj.id)
        self.assertTrue(test_obj.k.match({'z': 2}))
        self.assertFalse(test_obj.k.match({'z': 3}))

        # Once again, make sure we have a K object.
        self.assertTrue(isinstance(test_obj.k, K))

    def test_null_save(self):
        """
        Tests that null k patterns can be saved into a field specified with null=True.
        """
        # Verify that the creation returns a None
        test_obj = NullTrueModel.objects.create(k=None)
        self.assertIsNone(test_obj.k)

        # Verify that the value that was stored in the database was a json null, i.e. a string with the value 'null'
        # NO! That is NOT what we want! If the field is nullable, we should store a real null.
        # dbvalk = get_field_value('nulltruemodel', 'k')
        # self.assertEqual(dbvalk, 'null')
        # self.assertEqual(type(dbvalk), str)
        dbvalk = get_field_value('nulltruemodel', 'k')
        self.assertIsNone(dbvalk)

        # Make sure there is no difference with a value that was specified with a default=None
        dbvalknone = get_field_value('nulltruemodel', 'knone')
        self.assertIsNone(dbvalknone)

        # Verify that a Django queryset returns a None
        test_obj = NullTrueModel.objects.get(id=test_obj.id)
        self.assertIsNone(test_obj.k)

    def test_null_read(self):
        """
        Tests that k patterns previously saved into a field with a real database null value are ok
        """
        # Force insert into the null true model a row with real nulls
        sqlcmd = 'insert into tests_nulltruemodel (k, knone) values (null, null)'
        with connection.cursor() as cursor:
            cursor.execute(sqlcmd)

        # Verify that a Django queryset returns a None in this case, just like it would if it were a json null.
        test_obj = NullTrueModel.objects.last()
        self.assertIsNone(test_obj.k)

        # Set a column to a real k value and another column to None, and then save it.
        test_obj.k = ['==', 'a', 1]
        test_obj.knone = None
        test_obj.save()

        # Now the value should be a json null, right? Test directly from the db.
        dbvalknone = get_field_value('nulltruemodel', 'knone')
        self.assertIsNone(dbvalknone)

        # And look at it one more time from a queryset.
        test_obj = NullTrueModel.objects.get(id=test_obj.id)
        self.assertTrue(isinstance(test_obj.k, K))
        self.assertTrue(test_obj.k.match({'a': 1}))
        self.assertIsNone(test_obj.knone)

    def test_not_null(self):
        """
        Test failure when saving a null KField in a field specified as not null.
        This actually saves a "json null" i.e. the string "null" into the column.
        The column itself is not nullable at the database level, but accepts a None value all the same.
        """
        try:
            # Create a row in a not-nullable field with no value
            test_obj = KModel.objects.create()
        except IntegrityError as ie:
            print("Integrity error: ", ie)
        except Exception as e:
            print("Exception! (but not IntegrityError): ", e)
            import traceback
            traceback.print_stack()

        dbval = get_field_value('kmodel', 'k')
        self.assertEqual(dbval, 'null')
        self.assertEqual(type(dbval), str)

        test_obj = KModel.objects.get(id=test_obj.id)
        self.assertIsNone(test_obj.k)


    def test_invalid_pattern(self):
        """
        Tests accessing an invalid kmatch pattern.
        """
        with self.assertRaises(ValueError):
            KModel.objects.create(k='he(lo')

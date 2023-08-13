#!/usr/bin/python3
#!/usr/bin/python3
"""Unittest module for the BaseModel Class."""
import models
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from datetime import datetime
import json
import os
import re
from time import sleep
import unittest
import uuid


class TestBaseModel_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        ui1 = BaseModel()
        ui2 = BaseModel()
        self.assertNotEqual(ui1.id, ui2.id)

    def test_two_models_different_created_at(self):
        ui1 = BaseModel()
        sleep(0.05)
        ui2 = BaseModel()
        self.assertLess(ui1.created_at, ui2.created_at)

    def test_two_models_different_updated_at(self):
        ui1 = BaseModel()
        sleep(0.05)
        ui2 = BaseModel()
        self.assertLess(ui1.updated_at, ui2.updated_at)
    
    def test_str_representation(self):
        Date = datetime.today()
        Date_repr = repr(Date)
        base_model = BaseModel()
        base_model.id = "123456"
        base_model.created_at = base_model.updated_at = Date
        base_model_str = base_model.__str__()
        self.assertIn("[BaseModel] (123456)", base_model_str)
        self.assertIn("'id': '123456'", base_model_str)
        self.assertIn("'created_at': " + Date_repr, base_model_str)
        self.assertIn("'updated_at': " + Date_repr, base_model_str)
        
    def test_args_unused(self):
        base_model = BaseModel(None)
        self.assertNotIn(None, base_model.__dict__.values())

    def test_instantiation_with_kwargs(self):
        Date = datetime.today()
        Date_iso = Date.isoformat()
        bm = BaseModel(id="345", created_at=Date_iso, updated_at=Date_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, Date)
        self.assertEqual(bm.updated_at, Date)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        Date = datetime.today()
        Date_iso = Date.isoformat()
        bm = BaseModel("12", id="345", created_at=Date_iso, updated_at=Date_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, Date)
        self.assertEqual(bm.updated_at, Date)

class TestBaseModel_save(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""
    @classmethod
    def setUp(self):
        """Sets up test methods."""
        pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
    
    def test_first_save(self):
        base_model = BaseModel()
        sleep(0.05)
        first_updated_at = base_model.updated_at
        base_model.save()
        self.assertLess(first_updated_at, base_model.updated_at)

    def test_second_saves(self):
        base_model = BaseModel()
        sleep(0.05)
        first_updated_at = base_model.updated_at
        base_model.save()
        second_updated_at = base_model.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        base_model.save()
        self.assertLess(second_updated_at, base_model.updated_at)

    def test_save_with_arg(self):
        base_mode = BaseModel()
        with self.assertRaises(TypeError):
            base_mode.save(None)

    def test_save_updates_file(self):
        bm = BaseModel()
        bm.save()
        bmid = "BaseModel." + bm.id
        with open("file.json", "r") as f:
            self.assertIn(bmid, f.read())
    
class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        bm = BaseModel()
        self.assertTrue(dict, type(bm.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        bm = BaseModel()
        self.assertIn("id", bm.to_dict())
        self.assertIn("created_at", bm.to_dict())
        self.assertIn("updated_at", bm.to_dict())
        self.assertIn("__class__", bm.to_dict())

    def test_to_dict_contains_added_attributes(self):
        bm = BaseModel()
        bm.name = "BaseModel"
        bm.my_number = 98
        self.assertIn("name", bm.to_dict())
        self.assertIn("my_number", bm.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        bm = BaseModel()
        bm_dict = bm.to_dict()
        self.assertEqual(str, type(bm_dict["created_at"]))
        self.assertEqual(str, type(bm_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(bm.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        bm = BaseModel()
        self.assertNotEqual(bm.to_dict(), bm.__dict__)

    def test_to_dict_with_arg(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.to_dict(None)


if __name__ == '__main__':
    unittest.main()

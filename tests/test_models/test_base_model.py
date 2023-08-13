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


if __name__ == '__main__':
    unittest.main()


#!/usr/bin/python3
"""define filestorage"""
import json
import os

class FileStorage:
    """class for storing and retrieving data

    Attributes:
        __file_path (str): The name of the file save object to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):

        """sets in __objects the obj with key"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """ serializes __objects to the JSON file (path: __file_path)"""
        with open(FileStorage.__file_path, "w") as f:
            obj_dict = {j: i.to_dict() for j, i in FileStorage.__objects.items()}
            json.dump(obj_dict, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        if os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r") as f:
            file_dict = json.load(f)
            file_dict = {j: self.classes()[i["__class__"]](**i)
                        for j, i in file_dict.items()}
            FileStorage.__objects = file_dict


#!/usr/bin/python3
# base_model.py
# AbdulTechX
import uuid
from datetime import datetime
"""define a class BaseModel"""


class BaseModel:
    """Representing all common attributes/methods for 
    othe classes.
    """

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """updates the public instance attribute with the current datetime"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """returns a dictionary containing all keys/values of __dict__"""
        
        k_dict = self.__dict__.copy()
        k_dict["created_at"] = k_dict["created_at"].isoformat()
        k_dict["updated_at"] = k_dict["updated_at"].isoformat()
        k_dict["__class__"] = type(self).__name__
        return k_dict
    
    def __str__(self):
        """return the string representation format"""
        return "[{}] ({}) {}".\
            format(type(self).__name__, self.id, self.__dict__)

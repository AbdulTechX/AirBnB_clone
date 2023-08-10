#!/usr/bin/python3
# base_model.py
# AbdulTechX
import uuid
from datetime import datetime
from models import storage
"""define a class BaseModel"""


class BaseModel:
    """Representing all common attributes/methods for
    other classes.
    """

    def __init__(self, *args, **kwargs):
        """initializing instance attribute

        Args:
            *args: list of argument such as (hnb$ hello ,
            welcome)
            First argument : Hello
            Next argument through *argv : Welcome
            **kwargs: list of keyword argument (dict)
            such as (hnb$ first_name: Abdul,
            second_name: buhari)

        """
        timeformat = "%Y-%m-%dT%H:%M:%S.%f"
        if kwargs is not None and kwargs != {}:
            for keyword in kwargs:
                if keyword == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], timeformat)
                elif keyword == "updated_at":
                    self.__dict__["update_at"] = datetime.strptime(
                        kwargs["created_at"], timeformat)
                else:
                    self.__dict__[keyword] = kwargs[keyword]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def save(self):
        """updates the public instance attribute with the current datetime"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of __dict__"""

        k_dict = self.__dict__.copy()
        k_dict["__class__"] = type(self).__name__
        k_dict["created_at"] = k_dict["created_at"].isoformat()
        k_dict["updated_at"] = k_dict["updated_at"].isoformat()
        return k_dict

    def __str__(self):
        """return the string representation format"""
        return "[{}] ({}) {}".\
            format(type(self).__name__, self.id, self.__dict__)

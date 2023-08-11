#!/usr/bin/python3
# amenity.py
# AbdulTechX
""""Define a class User that inhert from BaseModel"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Represent a Amenity.

    Attributes:
           name(str): the name of the type of amenity
    """
    name = ""

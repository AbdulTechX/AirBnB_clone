#!/usr/bin/python3
# city.py
# AbdulTechX
""""Define a class User that inhert from BaseModel"""
from models.base_model import BaseModel


class City(BaseModel):
    """Represent a City.

    Attributes:
           state_id(str): the state unique id
           name(str): city name
    """
    state_id = ""
    name = ""

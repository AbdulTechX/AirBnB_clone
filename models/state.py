#!/usr/bin/python3
# state.py
# AbdulTechX
""""Define a class User that inhert from BaseModel"""
from models.base_model import BaseModel


class State(BaseModel):
    """Represent a User.

    Attributes:
           name(str): the name of the state
    """
    name = ""

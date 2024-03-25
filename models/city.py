#!/usr/bin/python3
"""
Module for City class.
"""
from models.base_model import BaseModel


class City(BaseModel):
    """
    City class that inherits from BaseModel.
    Public class attributes:
        state_id: string - empty string: it will be the State.id
        name: string - empty string
    """
    state_id = ""
    name = ""

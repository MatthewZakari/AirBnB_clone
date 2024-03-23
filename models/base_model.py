#!/usr/bin/python3
"""
BaseModel Module
"""
import uuid
from datetime import datetime


class BaseModel:
    """
    BaseModel class
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of BaseModel
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ['created_at', 'updated_at']:
                        setattr(self, key, datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f'))
                    else:
                        setattr(self, key, value)
            if 'created_at' not in kwargs:
                self.created_at = datetime.now()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """
        Returns string representation of the object
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                self.id, self.__dict__)

    def save(self):
        """
        Updates pub instance attribute updated_at with the current datetime
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        Returns dict. containing all keys/values of __dict__ of the instance
        """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict

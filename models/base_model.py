#!/usr/bin/python3
"""
BaseModel Module
"""
import models
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
        time_form = '%Y-%m-%dT%H:%M:%S.%f'
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ['created_at', 'updated_at']:
                        setattr(self, key, datetime.strptime(value, time_form))
                    else:
                        setattr(self, key, value)
        else:
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

        models.storage.new(self)

    def save(self):
        """
        Updates pub instance attribute updated_at with the current datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Returns dict. containing all keys/values of __dict__ of the instance
        """
        obj_dict = self.__dict__.copy()
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        obj_dict['__class__'] = self.__class__.__name__
        return obj_dict

    def __str__(self):
        """
        Returns string representation of the object
        """
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)


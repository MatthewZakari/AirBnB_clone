#!/usr/bin/python3
"""
FileStorage Module
"""
import json
from models.base_model import BaseModel


class FileStorage:
    """
    FileStorage class
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Returns the dictionary __objects
        """
        return self.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path)
        """
        serializable = {key: value.to_dict()
                        for key, value in self.__objects.items()}
        with open(self.__file_path, 'w') as file:
            json.dump(serializable, file)

    def reload(self):
        """
        Deserializes JSON file to __objects (only if (__file_path) exists)
        """
        try:
            with open(self.__file_path, 'r') as file:
                data = json.load(file)
                for key, value in data.items():
                    class_name, obj_id = key.split('.')
                    self.__objects[key] = eval(class_name)(**value)
        except FileNotFoundError:
            pass


"""Instantiate the storage object at the module level"""
storage = FileStorage()
storage.reload()

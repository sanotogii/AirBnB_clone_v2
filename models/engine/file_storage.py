#!/usr/bin/python3
"""file_storage
This module defines the BaseModel class.
Classes:
    - FileStorage: A class for storing and retrieving data
"""
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json

classes = {
    "BaseModel": BaseModel,
    "User": User,
    "Place": Place,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Review": Review
}
"""classes: dictionary mapping class names to corresponding class objects"""


class FileStorage:
    """Serializes and deserializes JSON file"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Get all objects stored in the file.
        Returns:
            the dictionary __objects
        """
        return self.__objects

    def new(self, obj):
        """Add a new object to the storage
        Description:
            Sets in __objects the obj with key <obj class name>.id.
        Args:
            obj: The object to be added.
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        serialized_objects = {}
        for key, obj in self.__objects.items():
            serialized_objects[key] = obj.to_dict()
        with open(self.__file_path, 'w', encoding='utf-8') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as file:
                deserialized_objects = json.load(file)
                for key, obj_dict in deserialized_objects.items():
                    class_name = obj_dict['__class__']
                    self.__objects[key] = classes[class_name](**obj_dict)
        except FileNotFoundError:
            pass


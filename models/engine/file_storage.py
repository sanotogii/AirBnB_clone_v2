#!/usr/bin/python3
"""
FileStorage module
"""
import json
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
    """ FileStorage class """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """ Return all objects or objects of a specific class """
        if cls is None:
            return self.__objects
        return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}

    def new(self, obj):
        """ Add new object to storage """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def delete(self, obj=None):
        """ Delete an object from storage """
        if obj is None:
            return
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects.pop(key, None)

    def save(self):
        """ Save objects to file """
        with open(self.__file_path, mode="w", encoding="utf-8") as file:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, file)

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

    def close(self):
        """ Call reload() method for deserializing the JSON file to objects """
        self.reload()

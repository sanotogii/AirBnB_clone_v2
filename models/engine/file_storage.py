#!/usr/bin/python3
"""
FileStorage module
"""
import json


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
            json.dump(
                {k: v.to_dict() for k, v in self.__objects.items()}, 
                file)

    def reload(self):
        """ Reload objects from file """
        try:
            with open(self.__file_path, mode="r", encoding="utf-8") as file:
                objs = json.load(file)
                self.__objects = {
                    k: eval(v["__class__"])(**v) for k, v in objs.items()
                    }
        except FileNotFoundError:
            pass

    def close(self):
        """ Call reload() method for deserializing the JSON file to objects """
        self.reload()

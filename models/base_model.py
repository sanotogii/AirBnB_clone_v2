#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime


class BaseModel:
    """A base class for all hbnb models"""

    def __init__(self, **kwargs):

        """
        Initializes a new instance of the BaseModel class.

        Attributes:
            - id (str): Unique identifier for the instance.
            - created_at (datetime): Date and time of instance creation.
            - updated_at (datetime): Date and time of last update.
        """
        if not kwargs:
            # Handle the case when no kwargs are provided
            # For example, when creating a new instance without arguments
            print("Creating an empty instance of BaseModel")
        else:
            # Extract required attributes from kwargs or set default values
            self.id = kwargs.get('id', str(uuid.uuid4()))
            self.created_at = kwargs.get('created_at', datetime.now())
            self.updated_at = kwargs.get('updated_at', datetime.now())

            # Handle arbitrary attributes using kwargs
            for key, value in kwargs.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(self, key, value)

        # if kwargs:
        #     # Reconstruct an instance from a dictionary representation
        #     if "__class__" in kwargs:
        #         del kwargs["__class__"]  # Remove __class__ from the dictionary
        #     # convert to datetime objects
        #     kwargs["created_at"] = datetime.strptime(kwargs["created_at"],
        #                                              "%Y-%m-%dT%H:%M:%S.%f")
        #     kwargs["updated_at"] = datetime.strptime(kwargs["updated_at"],
        #                                              "%Y-%m-%dT%H:%M:%S.%f")

        #     # Assign the values to instance attributes
        #     for key, value in kwargs.items():
        #         setattr(self, key, value)

        # else:
        #     from models import storage
        #     self.id = str(uuid.uuid4())
        #     self.created_at = datetime.now()
        #     self.updated_at = datetime.now()
        #     storage.new(self)
        #     storage.save()

    # def __init__(self, *args, **kwargs):

    #     """Instatntiates a new model"""

    #     if not kwargs:
    #         from models import storage
    #         self.id = str(uuid.uuid4())
    #         self.created_at = datetime.now()
    #         self.updated_at = datetime.now()
    #         storage.new(self)
    #     else:
    #         kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
    #                                                  '%Y-%m-%dT%H:%M:%S.%f')
    #         kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
    #                                                  '%Y-%m-%dT%H:%M:%S.%f')
    #         del kwargs['__class__']
    #         self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary
    
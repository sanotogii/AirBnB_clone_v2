#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""


from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from os import getenv

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """interaacts with the MySQL database"""
        __engine = None
        __session = None

        def __init__(self):
            """Instantiate a DBStorage object"""
            HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
            HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
            HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
            HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
            HBNB_ENV = getenv('HBNB_ENV')
            self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                        format(HBNB_MYSQL_USER,
                                                HBNB_MYSQL_PWD,
                                                HBNB_MYSQL_HOST,
                                                HBNB_MYSQL_DB))
            if HBNB_ENV == "test":
                Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries all objects depending on the class name.
        Returns a dictionary.
        """
        obj_dict = {}
        if cls:
            query_objs = self.__session.query(cls).all()
        else:
            query_objs = []
            for table_cls in [User, State, City, Amenity, Place, Review]:
                query_objs.extend(self.__session.query(table_cls).all())

        for obj in query_objs:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            obj_dict[key] = obj

        return obj_dict

    def new(self, obj):
        """
        Adds the object to the current database session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits all changes of the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes the object from the current database session if not None.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Creates all tables in the database and creates the current database session.
        """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                               expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """ Calls remove() on the private session attribute """
        self.__session.close()
        self.reload()

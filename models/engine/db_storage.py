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
from os import environ


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes DBStorage instance.
        """
        # Retrieve environment variables
        user = environ.get('HBNB_MYSQL_USER')
        password = environ.get('HBNB_MYSQL_PWD')
        host = environ.get('HBNB_MYSQL_HOST', 'localhost')
        db = environ.get('HBNB_MYSQL_DB')

        # Create engine
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, password, host, db),
                                      pool_pre_ping=True)

        # Drop all tables if HBNB_ENV is test
        if environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

        # Create all tables in the database
        Base.metadata.create_all(self.__engine)

        # Create a scoped session
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                               expire_on_commit=False))
        self.__session = Session()

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
#!/usr/bin/python3
"""Database engine"""
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import Session
import os


class DBStorage:
    """ BDSTorage class """

    __engine = None
    __session = None

    def __init__(self):
        """ Initialize the DBStorage """
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
            pool_pre_ping=True
        )

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Return all objects or objects of a specific class """
        from models import state, city
        session = self.__session
        objects = {}

        if cls is None:
            classes = [state.State, city.City]
        else:
            classes = [cls]

        for c in classes:
            objs = session.query(c).all()
            for obj in objs:
                key = f"{obj.__class__.__name__}.{obj.id}"
                objects[key] = obj

        return objects

    def new(self, obj):
        """ Add new object to storage """
        self.__session.add(obj)

    def save(self):
        """ Save objects to file """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete an object from storage """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        Call remove() method on the private session
        attribute (self.__session)
        """
        self.__session.remove()

#!/usr/bin/python3
"""Database engine"""
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from sqlalchemy import create_engine
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """database engine"""

    __engine = None
    __session = None

    def __init__(self):
        """the init method"""
        username = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        hbnb_env = getenv("HBNB_ENV")

        self.__engine = create_engine(f"mysql+mysqldb://{username}:{passwd}\
                                      @host:{host}/{db}", pool_pre_ping=True)
        if hbnb_env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects of a certain type if cls=None, query all types"""

        result = {}
        if cls:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = type(obj).__name__ + "." + str(obj.id)
                result[key] = obj
        else:
            classes = [User, State, City, Amenity, Place, Review]
            for cls in classes:
                objs = self.__session.query(cls).all()
                for obj in objs:
                    key = type(obj).__name__ + "." + str(obj.id)
                    result[key] = obj
        return result

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database & current database session"""
        Base.metadata.create_all(self.__engine)
        s_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(s_factory)
        self.__session = Session()

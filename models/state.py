#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
import os
from dotenv import load_dotenv

load_dotenv()


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        @property
        def cities(self):
            """ Getter method for cities """
            from models import storage
            cities_list = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
    else:
        cities = relationship("City", backref="state", cascade="all, delete")

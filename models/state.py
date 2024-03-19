#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "State"
    name = Column(String(128), nullable=False)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship('City', cascade='all, delete', backref='state')
    else:
        @property
        def cities(self):
            from models import storage
            all_cities = storage.all(City)
            return [c for c in all_cities.values() if c.state_id == self.id]

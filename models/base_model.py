#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

# Create a base class for SQLAlchemy models
Base = declarative_base()

class BaseModel:
    """BaseModel class representing the base for all models"""

    # Define columns for id, created_at, and updated_at
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize BaseModel instance"""
        # Generate a unique ID for the object
        self.id = str(uuid.uuid4())
        # Set the creation and update timestamps to the current time
        self.created_at = self.updated_at = datetime.datetime.now()
        # Assign any additional keyword arguments passed to the constructor as attributes
        for k, v in kwargs.items():
            setattr(self, k, v)

    def save(self):
        """Save the object to the database"""
        # Import storage module to access storage methods
        from models import storage
        # Add the object to storage and save changes
        storage.new(self)
        storage.save()

    def delete(self):
        """Delete the object from the database"""
        # Import storage module to access storage methods
        from models import storage
        # Delete the object from storage
        storage.delete(self)
    
    def to_dict(self):
        """Convert object attributes to dictionary"""
        # Create a dictionary containing object attributes
        data = dict(self.__dict__)
        # Remove SQLAlchemy internal state attribute
        data.pop('_sa_instance_state', None)
        return data

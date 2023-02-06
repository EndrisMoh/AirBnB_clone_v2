#!/usr/bin/python3

"""This is the state class"""
from models.base_model import BaseModel, Base
from models.city import City
from models import storage_type
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = 'states'

    if storage_type == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", cascade="all", backref="state")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if storage_type != 'db':
        @property
        def cities(self):
            """returns city list instead"""
            result = []
            for i in models.storage.all(City).values():
                if i.state_id == self.id:
                    result.append(i)
            return result

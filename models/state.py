#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    __tablename__ = 'states'
    """ State class """
    name = Column(String(128), nullable=False)

    if getenv('HBNB_TYPE_STORAGE') == db:
        cities = relationship('City', backref='state', cascade='all, delete-orphan')
    else:
        @property
        def cities(self):
            """FileStorage relationship between State and City"""
            import models
            from models.city import City


            list_city_list = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    list_city_list.append(City)

            return list_city_list

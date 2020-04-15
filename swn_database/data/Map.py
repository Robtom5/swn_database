
#! /usr/bin/env python3
from .ISerializable import ISerializable
from collections import namedtuple

Point = namedtuple('Point','x y')

# Map is visualisation not data and should not be serialized as it can be created from our data, 
# Point, or better, coordinate, is data so should exist here
class Map(ISerializable):
    def __init__(self):
        self.Planets = []
        self.Connections = []
        self._Ids = []

    def create_planet():
        pass

    def create_connection():
        pass

    def add_planet():
        pass

    def add_connection():
        pass

    @property
    def ID(self):
        return self._ID

    @classmethod
    def deserialize(cls, string_representation: str):
        """Deserialize the class from a string"""
        raise NotImplementedError

    def serialize(self) -> str:
        """Serialize an instance of the class as a string"""
        raise NotImplementedError

    class __IdGenerator():
        def __init__(self):
            self.count = 0

        def __call__(self):
            self.count += 1
            return self.count
#! /usr/bin/env python3
import sqlite3
from .ISerializable import ISerializable
from .DataStructures import Coordinate


class Planet(ISerializable):

    def __init__(self, name: str, coords: Coordinate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._Coordinates = coords
        self.Name = name

    @property
    def Coordinates(self):
        return self._Coordinates

    @classmethod
    def deserialize(cls, string_representation: str):
        """Deserialize the class from a string"""

        pass

    def serialize(self) -> str:
        """Serialize an instance of the class as a string"""
        pass

    def __str__(self):
        return f"{self._Coordinates} - {self.Name:<3}"

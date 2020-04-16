#! /usr/bin/env python3
import sqlite3
from .ISerializable import ISerializable


class Connection(ISerializable):
    def __init__(self, ID_Planet_1: int, ID_Planet_2: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ID_Planet_1 = ID_Planet_1
        self.ID_Planet_2 = ID_Planet_2

    def __eq__(self, other):
        """Override of equality comparison"""
        if isinstance(other, Connection):
            return (other.ID == self.ID
                    and (other.ID_Planet_1 == self.ID_Planet_1 or other.ID_Planet_1 == self.ID_Planet_2)
                    and (other.ID_Planet_2 == self.ID_Planet_1 or other.ID_Planet_2 == self.ID_Planet_2))
        return False

    @classmethod
    def fromPlanets(cls, ID: int, planet_1, planet_2):
        return Connection(ID=ID, ID_Planet_1=planet_1.ID, ID_Planet_2=planet_2.ID)

    @property
    def ID(self):
        return self._ID

    @classmethod
    def deserialize(cls, string_representation: str):
        """Deserialize the class from a string"""
        connection_ID, planet_1, planet_2 = map(
            int, string_representation.split(";"))
        return Connection(ID=connection_ID, ID_Planet_1=planet_1, ID_Planet_2=planet_2)

    def serialize(self) -> str:
        """Serialize an instance of the class as a string"""
        return (f"{self.ID};{self.ID_Planet_1};{self.ID_Planet_2}")

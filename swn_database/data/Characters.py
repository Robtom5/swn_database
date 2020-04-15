#! /usr/bin/env python3
import sqlite3
from .ISerializable import ISerializable
import abc


class CharacterBase(metaclass=abc.ABCMeta):
    def __init__(self, id: int,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ID = id

    @property
    def ID(self):
        return self._ID

    @property
    def AC(self):
        return self._AC

    @property
    def Atk(self):
        return self._Atk

    @abc.abstractproperty
    def Name(self):
        raise NotImplementedError


class PlayerCharacter(CharacterBase, ISerializable):
    def __init__(self, id: int):
        super(CharacterBase, self).__init__()

    @property
    def Name(self):
        return self._Name

    @classmethod
    def deserialize(cls, string_representation: str):
        """Deserialize the class from a string"""

        pass

    def serialize(self) -> str:
        """Serialize an instance of the class as a string"""
        pass


class NonPlayerCharacter(CharacterBase, ISerializable):
    @property
    def Name(self):
        return self._Name

    @classmethod
    def deserialize(cls, string_representation: str):
        """Deserialize the class from a string"""

        pass

    def serialize(self) -> str:
        """Serialize an instance of the class as a string"""
        pass

    pass

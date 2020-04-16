#! /usr/bin/env python3
import sqlite3
from .ISerializable import ISerializable
from .DataStructures import DiceRoll
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

    @property
    def Move(self):
        return self._Move

    @abc.abstractproperty
    def Name(self):
        raise NotImplementedError


class PlayerCharacter(CharacterBase, ISerializable):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def Name(self):
        return self._Name

    @classmethod
    def deserialize(cls, string_representation: str):
        """Deserialize the class from a string"""
        raise NotImplementedError()

    def serialize(self) -> str:
        """Serialize an instance of the class as a string"""
        raise NotImplementedError()


class NonPlayerCharacter(CharacterBase, ISerializable):
    def __init__(self, name: str, morale: int = 6, skillmod: int = 0, savetarget: int = 15,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._Name = name
        self._ML = morale
        if skillmod < 0:
            self._Skills = DiceRoll(f"1d20 {skillmod}")
        else:
            self._Skills = DiceRoll(f"1d20 + {skillmod}")
        self._Saves = savetarget

    @property
    def Name(self):
        return self._Name

    @property
    def ML(self):
        return self._ML

    @property
    def Skills(self):
        return self._Skills

    @property
    def Saves(self):
        return self._Saves

    @classmethod
    def deserialize(cls, string_representation: str):
        """Deserialize the class from a string"""
        raise NotImplementedError()

    def serialize(self) -> str:
        """Serialize an instance of the class as a string"""
        raise NotImplementedError()

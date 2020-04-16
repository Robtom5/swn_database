#! /usr/bin/env python3
import sqlite3
from .ISerializable import ISerializable
from .DataStructures import DiceRoll, AttackRoll
import abc


class CharacterBase(ISerializable, metaclass=abc.ABCMeta):
    def __init__(self, ac: int = 10, atk: int = 0, move: int = 10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._AC = ac
        self._Atk = AttackRoll.FromModifier(atk)
        self._Move = move

    @property
    def AC(self):
        return self._AC

    @property
    def Atk(self):
        return self._Atk

    @property
    def Move(self):
        '''Returns the number of meters this character can move in one round'''
        return self._Move

    @abc.abstractproperty
    def Name(self):
        raise NotImplementedError


class PlayerCharacter(CharacterBase):
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


class NonPlayerCharacter(CharacterBase):
    def __init__(self, name: str, morale: int = 6, skillmod: int = 0, savetarget: int = 15,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._Name = name
        self._ML = morale
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

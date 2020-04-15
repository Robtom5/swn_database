#! /usr/bin/env python3
import sqlite3
from .ISerializable import ISerializable
import abc

class ItemBase(metaclass=abc.ABCMeta):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)


class Weapon(ItemBase, ISerializable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def Range(self):
        return self._Range
    
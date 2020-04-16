#! /usr/bin/env python3
import sqlite3
from .ISerializable import ISerializable
from .DataStructures import DiceRoll
import abc


class Item(ISerializable):
    def __init__(self,
                 *,
                 name: str,
                 cost: int = 0,
                 enc: int = 1,
                 tl: int = 4,
                 packable: bool = False,
                 **kwargs):
        super().__init__(**kwargs)
        self._Name = name.replace(";", "")
        self._Cost = cost
        self._Encumbrance = enc % 10  # We dont support encumberances >9 or <0
        self._TL = tl % 6  # Tl should be between 0 and 5
        self._Packable = packable

    @property
    def Name(self):
        return self._Name

    @property
    def Cost(self):
        return self._Cost

    @property
    def Encumbrance(self):
        return self._Encumbrance

    @property
    def TL(self):
        return self._TL

    @property
    def Packable(self):
        '''Returns if the item can be bundled together'''
        return self._Packable

    @classmethod
    def deserialize(cls, query_result: str):
        """Deserialize the class from a sql query result"""
        ID = int(query_result[0])
        name = query_result[1]
        cost =  int(query_result[2])
        enc =  int(query_result[3])
        tl =  int(query_result[4])
        packable = bool(query_result[5])
        return Item(ID=ID, name=name, cost=cost, enc=enc, tl=tl, packable=packable)

    def serialize(self) -> str:
        """Serialize an instance of the class as a string"""
        return (self.ID, self.Name, self.Cost, self.Encumbrance, self.TL, int(self.Packable))

    def __eq__(self, other):
        if isinstance(other, Item):
            return other.serialize() == self.serialize()
        return False


class Weapon(Item, metaclass=abc.ABCMeta):
    def __init__(self,
                 *,
                 damage: str = "1d6",
                 attr: str="STR/DEX",
                 **kwargs):
        super().__init__(**kwargs)

        self._Damage = DiceRoll(damage)
        self._Attribute = attr

    @property
    def Damage(self):
        return self._Damage

    @property
    def Attribute(self):
        return self._Attribute


class MeleeWeapon(Weapon):
    def __init__(self,
                 *,
                 shock_dmg: int = 1,
                 shock_thresh: int = 15,
                 **kwargs):
        self._Shock_Damage = shock_dmg
        self._Shock_Threshold = shock_thresh

    @property
    def Shock_Damage(self):
        return self._Shock_Damage

    @property
    def Shock_Threshold(self):
        return self._Shock_Threshold


class RangedWeapon(Weapon):
    def __init__(self,
                 *,
                 mag: int = 1,
                 range_short: int=0,
                 range_long: int=10,
                 burst: bool = False,
                 slow_reload: bool = False,
                 energy_weapon: bool = False,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self._Mag = mag
        self._Range_Short = range_short
        self._Range_Long = range_long
        self._Burst = burst
        self._Slow_Reload = slow_reload
        self._Energy_Weapon = energy_weapon

    @property
    def Mag(self):
        return self._Mag

    @property
    def Range_Short(self):
        return self._Range_Short

    @property
    def Range_Long(self):
        return self._Range_Long

    @property
    def Burst(self):
        return self._Burst

    @property
    def Slow_Reload(self):
        return self._Slow_Reload

    @property
    def Energy_Weapon(self):
        return self._Energy_Weapon


class HeavyWeapon(Weapon):
    def __init__(self,
                 can_suppress: bool = False,
                 vehicle_only: bool = False,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._Can_Suppress = can_suppress
        self._Vehicle_Only = vehicle_only

    @property
    def Can_Suppress(self):
        return self._Can_Suppress

    @property
    def Vehicle_Only(self):
        return self._Vehicle_Only

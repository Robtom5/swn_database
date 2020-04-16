#! /usr/bin/env python3
import sqlite3
from .ISerializable import ISerializable
from .DataStructures import DiceRoll
import abc


class Item(ISerializable):
    def __init__(self,
                 name: str,
                 cost: int = 0,
                 enc: int = 1,
                 tl: int = 4,
                 packable: bool = False,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._Name = name
        self._Cost = cost
        self._Encumbrance = enc
        self._tl = tl
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


class Weapon(Item, metaclass=abc.ABCMeta):
    def __init__(self,
                 damage: str = "1d6",
                 attr: str="STR/DEX",
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

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
                 shock_dmg: int = 1,
                 shock_thresh: int = 15,
                 *args, **kwargs):
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
                 mag: int = 1,
                 range_short: int=0,
                 range_long: int=10,
                 burst: bool = False,
                 slow_reload: bool = False,
                 energy_weapon: bool = False,
                 *args, **kwargs):
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
    

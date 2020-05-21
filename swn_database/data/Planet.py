#! /usr/bin/env python3
from .ISerializable import ISerializable
from .DataStructures import Coordinate


class Planet(ISerializable):

    def __init__(self,
                 *,
                 name: str,
                 coords: Coordinate,
                 tl: int,
                 bio: int,
                 atmos: int,
                 temp: int,
                 pop: int,
                 description: str,
                 notes: str,
                 **kwargs):
        super().__init__(**kwargs)
        self._name = name.replace(";", "")
        self._coordinates = coords
        self._tl = tl
        self._biosphere = bio
        self._atmosphere = atmos
        self._temperature = temp
        self._population = pop
        self.description = description
        self.notes = notes

    @property
    def name(self):
        return self._name

    @property
    def coordinates(self):
        return self._coordinates

    @property
    def tl(self):
        return self._tl

    @property
    def biosphere(self):
        return self._biosphere

    @property
    def atmosphere(self):
        return self._atmosphere

    @property
    def temperature(self):
        return self._temperature

    @property
    def population(self):
        return self._population

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        if val is not None:
            val = val.replace(";", "")
        self._description = val

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, val):
        if val is not None:
            val = val.replace(";", "")
        self._notes = val

    @classmethod
    def deserialize(cls, serialized_data: tuple):
        """Deserialize the class from a string"""
        ID = serialized_data[0]
        name = serialized_data[1]
        coords = Coordinate.from_hex(
            serialized_data[2]) if serialized_data[2] else None
        tl = serialized_data[3]
        bio = serialized_data[4]
        atmos = serialized_data[5]
        temp = serialized_data[6]
        pop = serialized_data[7]
        desc = serialized_data[8]
        notes = serialized_data[9]
        return Planet(
            ID=ID,
            name=name,
            coords=coords,
            tl=tl,
            bio=bio,
            atmos=atmos,
            temp=temp,
            pop=pop,
            description=desc,
            notes=notes)

    def serialize(self) -> tuple:
        """Serialize an instance of the class as a string"""
        return (self.ID, self.name, self.coordinates, self.tl, self.biosphere,
                self.atmosphere, self.temperature, self.population, self.description, self.notes)

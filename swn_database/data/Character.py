#! /usr/bin/env python3

class Character():
    def __init__(self,
                 *,
                 ID,
                 name,
                 surname,
                 age=None,
                 homeworld=None,
                 curr_world=None,
                 description=None,
                 notes=None,
                 trustworthiness=None,
                 desire=None,
                 isPC=False,
                 role=None,
                 **kwargs):
        super().__init__(**kwargs)
        self._ID = ID
        self._name = name
        self._surname = surname
        self._age = age
        self._homeworld = homeworld
        self._current_planet = curr_world
        self._description = description
        self._notes = notes
        self._trustworthiness = trustworthiness
        self._desire = desire
        self._isPC = isPC
        self._role = role

    @property
    def ID(self):
        return self._ID

    @property
    def name(self):
        return self._name

    @property
    def surname(self):
        return self._surname

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, val):
        if val > 0:
            self._age = val
        else:
            raise ValueError("Age must be greater than 0")

    @property
    def homeworld(self):
        return self._homeworld

    @homeworld.setter
    def homeworld(self, val):
        self._homeworld = val

    @property
    def current_planet(self):
        return self._current_planet

    @current_planet.setter
    def current_planet(self, val):
        self._current_planet = val

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

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, val):
        if val is not None:
            val = val.replace(";", "")
        self._role = val

    @property
    def trustworthiness(self):
        return self._trustworthiness

    @property
    def desire(self):
        return self._desire

    @property
    def isPC(self):
        return self._isPC

    def serialize(self):
        return (self.name,
                self.surname,
                self.age,
                self.homeworld,
                self.current_planet,
                self.description,
                self.notes,
                self.trustworthiness,
                self.desire,
                self.isPC)

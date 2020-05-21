#! /usr/bin/env python3
from ..data import Character
from .Factory import Factory


class CharacterFactory(Factory):
    @staticmethod
    def create(serialized_data: tuple):
        character_id = serialized_data[0]
        name = serialized_data[1]
        surname = serialized_data[2]
        age = serialized_data[3]
        homeworld = serialized_data[4]
        curr_world = serialized_data[5]
        description = serialized_data[6]
        notes = serialized_data[7]
        trustworthiness = serialized_data[8]
        desire = serialized_data[9]
        isPC = bool(serialized_data[10])
        role = serialized_data[11]
        return Character(
            ID=character_id,
            name=name,
            surname=surname,
            age=age,
            homeworld=homeworld,
            curr_world=curr_world,
            description=description,
            notes=notes,
            trustworthiness=trustworthiness,
            desire=desire,
            isPC=isPC,
            role=role)

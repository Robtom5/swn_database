#! /usr/bin/env python3
import pytest
from swn_database.data import Planet, Coordinate

def test_serialize_returnsExpectedTuple():
    expected = (1, "TestPlanet", "A2", 2, 3, 4, 5, 6, "A planet", "notes")
    planet = Planet(ID=1, name="TestPlanet", coords="A2", tl=2, bio=3, atmos=4, temp=5, pop=6, description="A planet", notes="notes")
    serialized = planet.serialize()
    assert expected == serialized

def test_deserialize_returnsExpectedPlanet():
    serialized = (1, "TestPlanet", "A2", 2, 3, 4, 5, 6, "A planet", "notes")
    planet = Planet.deserialize(serialized)

    assert planet.ID == 1
    assert planet.name == "TestPlanet"
    assert planet.coordinates == Coordinate.from_hex("A2")
    assert planet.tl == 2
    assert planet.biosphere == 3
    assert planet.atmosphere == 4
    assert planet.temperature == 5
    assert planet.population == 6
    assert planet.description == "A planet"
    assert planet.notes == "notes"
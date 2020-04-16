#! /usr/bin/env python3
import pytest
from swn_database.data import PlayerCharacter, NonPlayerCharacter

def test_PlayerCharacter_Constructor_DoesNotThrow():
    pc = PlayerCharacter(ID = 2)

def test_NonPlayerCharacter_Constructor_DoesNotThrow():
    npc = NonPlayerCharacter(ID = 1, name = "test")
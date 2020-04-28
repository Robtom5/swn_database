#! /usr/bin/env python3
import pytest
from swn_database.data.DataStructures import Coordinate, DiceRoll, AttackRoll

DICEROLL_STRING = "1d20 + 2"


@pytest.fixture
def coordinate():
    return Coordinate(30, 45)


def test_Coordinate_str_ReturnsExpectedHexRepresentation(coordinate):
    assert f"{coordinate}" == "AD45"


def test_Coordinate_From_Hex_ReturnsCoordinateWithCorrectValues():
    hex_string = "AB34"
    coord = Coordinate.from_hex(hex_string)
    assert coord.x == 28
    assert coord.y == 34


def test_Coordinate_From_Hex_ThrowsValueError_WhenGivenInvalidHexString():
    with pytest.raises(ValueError) as e_info:
        Coordinate.from_hex("invalid")

def test_Coordinate_eq_returnsTrueIfBothHaveSameValues():
    first_coord = Coordinate(20, 19)
    second_coord = Coordinate(20, 19)
    assert first_coord == second_coord

@pytest.fixture
def diceroll():
    return DiceRoll(DICEROLL_STRING)


def test_DiceRoll_DefaultConstructor_WorksAsExpected():
    dr = DiceRoll()


def test_DiceRoll_Roll_ReturnsExpectedValue():
    dr = DiceRoll("1d1")
    assert 1 == dr.Roll()


def test_DiceRoll_set_roll_string_ShouldCalculateOffset(diceroll: DiceRoll):
    expected_offset = 20
    diceroll.RollString = f"1d6 + {20}"
    assert expected_offset == diceroll.Mod
    diceroll.RollString = f"1d6 - {20}"
    assert -expected_offset == diceroll.Mod


def test_DiceRoll_set_roll_string_ThrowsValueErrorWhenNotGivenValidString(diceroll: DiceRoll):
    with pytest.raises(ValueError) as e_info:
        diceroll.RollString = "+2"


def test_DiceRoll_str_ReturnsRollStringAsRepresentation(diceroll: DiceRoll):
    assert f"{diceroll}" == DICEROLL_STRING

def test_AttackRoll_FromModifier_ReturnsCorrectResult():
    ar = AttackRoll.FromModifier(5)
    assert ar.Mod == 5
    assert ar.RollString == "1d20 + 5"

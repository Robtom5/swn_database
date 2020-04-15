#! /usr/bin/env python3
import pytest
from swn_database.data.DataStructures import Coordinate, DiceRoll


@pytest.fixture
def coordinate():
    return Coordinate(30, 45)


def test_Coordinate_str_ReturnsExpectedHexRepresentation(coordinate):
    assert f"{coordinate}" == "AD45"


def test_Coordinate_From_Hex_ReturnsCoordinateWithCorrectValues():
    hex_string = "AB34"
    coord = Coordinate.From_Hex(hex_string)
    assert coord.x == 28
    assert coord.y == 34


def test_Coordinate_From_Hex_ThrowsValueError_WhenGivenInvalidHexString():
    with pytest.raises(ValueError) as e_info:
        Coordinate.From_Hex("invalid")


@pytest.fixture
def diceroll():
    return DiceRoll("1d6")


def test_DiceRoll_DefaultConstructor_WorksAsExpected():
    dr = DiceRoll()


def test_DiceRoll_Roll_ReturnsExpectedValue():
    dr = DiceRoll("1d1")
    assert 1 == dr.Roll()


def test_DiceRoll_set_roll_string_ShouldCalculateOffset(diceroll: DiceRoll):
    expected_offset = 20
    assert 0 == diceroll._offset
    diceroll.roll_string = f"1d6 + {20}"
    assert expected_offset == diceroll._offset
    diceroll.roll_string = f"1d6 - {20}"
    assert -expected_offset == diceroll._offset


def test_DiceRoll_set_roll_string_ThrowsValueErrorWhenNotGivenValidString(diceroll: DiceRoll):
    with pytest.raises(ValueError) as e_info:
        diceroll.roll_string = "+2"

#! /usr/bin/env python3
import pytest
from swn_database.data import Connection, Coordinate


def create_connection(start_hex: str = "A1", end_hex: str="A2", conn_id: int=1) -> Connection:
    """Creates a new connection with the provided ids"""
    return Connection(start_hex=Coordinate.from_hex(start_hex), end_hex=Coordinate.from_hex(end_hex), conn_id=conn_id)


def test_constructor_setsPropertiesCorrectly():
    ID_Planet_1 = 1
    ID_Planet_2 = 2
    ID_Connection = 3

    con = Connection(start_hex=ID_Planet_1, end_hex=ID_Planet_2,
                     conn_id=ID_Connection)
    assert (con.connection_id == ID_Connection
            and con.start_hex == ID_Planet_1
            and con.end_hex == ID_Planet_2)



equalityTestData = [
    (("A1", "A2", 2), ("A1", "A2", 2), True),
    (("A1", "A2", 2), ("A2", "A1", 2), False),
    (("A1", "A2", 2), ("A1", "A2", 3), False)
]


@pytest.mark.parametrize("con_1_ids,con_2_ids,expected_equality", equalityTestData)
def test_equality_shouldReturnsExpectedResult(con_1_ids, con_2_ids, expected_equality):
    con_1 = create_connection(con_1_ids[0], con_1_ids[1], con_1_ids[2])
    con_2 = create_connection(con_2_ids[0], con_2_ids[1], con_2_ids[2])

    equality = con_1 == con_2

    assert equality == expected_equality


def test_equality_returnsFalseIfNotProvidedConnection():
    class Mock_Equatable():
        def __init__(self, start, end, conn):
            self.start_hex = Coordinate.from_hex(start)
            self.end_hex = Coordinate.from_hex(end)
            self.connection_id = conn

    con_1 = create_connection("A1", "A2", 1)
    con_2 = Mock_Equatable("A1", "A2", 1)
    assert (con_1 == con_2) == False


def test_serialize_returnsExpected():
    expected = ("A1", "A2", 1)
    con = create_connection()
    assert expected == con.serialize()

def test_str_returnsExpected():
    expected = "A1 -> A2"
    con = create_connection()
    assert expected == f"{con}"
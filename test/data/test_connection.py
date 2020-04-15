#! /usr/bin/env python3
import pytest
from swn_database.data import Connection


def create_connection(con_id: int = 3, plan_id_1: int = 1, plan_id_2: int = 2) -> Connection:
    """Creates a new connection with the provided ids"""
    return Connection(ID=con_id, ID_Planet_1=plan_id_1, ID_Planet_2=plan_id_2)


def test_constructor_setsPropertiesCorrectly():
    ID_Planet_1 = 1
    ID_Planet_2 = 2
    ID_Connection = 3

    con = Connection(ID=ID_Connection, ID_Planet_1=ID_Planet_1,
                     ID_Planet_2=ID_Planet_2)
    assert (con.ID == ID_Connection
            and con.ID_Planet_1 == ID_Planet_1
            and con.ID_Planet_2 == ID_Planet_2)


def test_fromPlanets_setsPropertiesCorrectly():
    class Mock_Planet(object):
        def __init__(self, ID: int):
            self.ID = ID

    ID_Planet_1 = 1
    ID_Planet_2 = 2
    ID_Connection = 3

    mockPlanet1 = Mock_Planet(ID_Planet_1)
    mockPlanet2 = Mock_Planet(ID_Planet_2)

    con = Connection.fromPlanets(ID_Connection, mockPlanet1, mockPlanet2)
    assert (con.ID == ID_Connection
            and con.ID_Planet_1 == ID_Planet_1
            and con.ID_Planet_2 == ID_Planet_2)


equalityTestData = [
    ((3, 1, 2), (3, 1, 2), True),
    ((3, 1, 2), (3, 2, 1), True),
    ((3, 1, 2), (3, 1, 3), False),
    ((3, 1, 2), (4, 1, 2), False),
]


@pytest.mark.parametrize("con_1_ids,con_2_ids,expected_equality", equalityTestData)
def test_equality_shouldReturnsExpectedResult(con_1_ids, con_2_ids, expected_equality):
    con_1 = create_connection(con_1_ids[0], con_1_ids[1], con_1_ids[2])
    con_2 = create_connection(con_2_ids[0], con_2_ids[1], con_2_ids[2])

    equality = con_1 == con_2

    assert equality == expected_equality


def test_equality_returnsFalseIfNotProvidedConnection():
    class Mock_Equatable():
        def __init__(self, id, planet1id, planet2id):
            self.ID = id
            self.ID_Planet_1 = planet1id
            self.ID_Planet_2 = planet2id

    con_1 = create_connection(3, 2, 1)
    con_2 = Mock_Equatable(3, 2, 1)
    assert (con_1 == con_2) == False


def test_serialize_returnsExpected():
    expected = "3;1;2"
    con = create_connection()
    assert expected == con.serialize()


def test_deserialize_returnsExpected():
    initial = create_connection()
    serialized = initial.serialize()
    deserialized = Connection.deserialize(serialized)
    assert initial == deserialized

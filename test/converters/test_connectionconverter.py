#! /usr/bin/env python3
import pytest
from swn_database.converters import ConnectionConverter
from swn_database.data import Connection, Coordinate


@pytest.fixture
def converter(sql_connection):
    return ConnectionConverter(sql_connection)


@pytest.fixture
def connection():
    return MockConnection()


def strip_whitespace(string):
    return ''.join(string.split())


class MockConnection():
    def __init__(self, start="A2", end="B2", conn_id=1):
        self.start_hex = start
        self.end_hex = end
        self.connection_id = conn_id


def test_create_table_query_ReturnsExpectedQuery(converter: ConnectionConverter):
    expected_query = """
            CREATE TABLE IF NOT EXISTS planetary_connections (
                start_hex TEXT NOT NULL,
                end_hex TEXT NOT NULL,
                connection_id INTEGER PRIMARY KEY AUTOINCREMENT,
                UNIQUE(start_hex, end_hex)
            );
            """
    assert strip_whitespace(
        converter.create_table_query) == strip_whitespace(expected_query)


def test_add_addsCorrectly(converter: ConnectionConverter, sql_connection):
    sql_connection.set_execute_read_results([[("A2", "B2", 1)]])
    returned_value = converter.add("A2", "B2")

    expected_query = """ INSERT INTO planetary_connections (
        start_hex,
        end_hex
    ) VALUES (
        'A2',
        'B2'
    ); 
    SELECT * FROM planetary_connections WHERE start_hex='A2' AND end_hex='B2'"""
    queries = sql_connection.get_queries()

    assert strip_whitespace(expected_query) == strip_whitespace(queries[0])
    assert returned_value.start_hex == Coordinate.from_hex("A2")
    assert returned_value.end_hex == Coordinate.from_hex("B2")
    assert returned_value.connection_id == 1


def test_add_returnsNoneIfFailsToAdd(converter: ConnectionConverter, sql_connection):
    sql_connection.set_execute_read_results([None, ])
    returned_value = converter.add("A2", "B3")
    assert returned_value == None


def test_load_by_id_loadsCorrectId(converter: ConnectionConverter, sql_connection, connection, monkeypatch):
    sql_connection.set_execute_read_results([("A1", "A2", 1)])

    with monkeypatch.context() as m:
        m.setattr('swn_database.data.Connection', MockConnection)
        m.setattr(
            'swn_database.data.DataStructures.Coordinate.from_hex', lambda n: n)
        returned_conn = converter.load_by_id(1)

    expected_query = "SELECT * FROM planetary_connections WHERE connection_id=1"
    queries = sql_connection.get_queries()
    load_query = queries[0]

    assert returned_conn.start_hex == "A1"
    assert returned_conn.end_hex == "A2"
    assert returned_conn.connection_id == 1
    assert strip_whitespace(expected_query) == strip_whitespace(load_query)


def test_load_all_loadsAll(converter: ConnectionConverter, sql_connection, connection, monkeypatch):
    sql_connection.set_execute_read_results([[("A1", "A2", 1)]])

    with monkeypatch.context() as m:
        m.setattr('swn_database.data.Connection', MockConnection)
        m.setattr(
            'swn_database.data.DataStructures.Coordinate.from_hex', lambda n: n)
        returned_item = converter.load_all()

    expected_query = "SELECT * FROM planetary_connections"
    queries = sql_connection.get_queries()
    load_query = queries[0]

    assert returned_item[0].start_hex == "A1"
    assert returned_item[0].end_hex == "A2"
    assert returned_item[0].connection_id == 1
    assert strip_whitespace(expected_query) == strip_whitespace(load_query)


def test_delete_deletes_connection(converter: ConnectionConverter, sql_connection, connection):
    converter.delete(connection.start_hex, connection.end_hex)
    queries = sql_connection.get_queries()
    delete_query = queries[0]

    expected_query = f"DELETE FROM planetary_connections WHERE start_hex='{connection.start_hex}' AND end_hex='{connection.end_hex}'"
    assert strip_whitespace(expected_query) == strip_whitespace(delete_query)


def test_create_bidirectional_connection_createsBothConnections(converter: ConnectionConverter, sql_connection):
    class MockPlanet():
        def __init__(self, coordinates):
            self.coordinates = coordinates

    expected_query = """ INSERT INTO planetary_connections (start_hex,end_hex) 
    VALUES ('A2', 'B2'), ('B2', 'A2');"""
    planet_1 = MockPlanet("A2")
    planet_2 = MockPlanet("B2")

    converter.create_bidirectional_connection(planet_1, planet_2)

    queries = sql_connection.get_queries()
    add_query = queries[0]

    assert strip_whitespace(add_query) == strip_whitespace(expected_query)


def test_delete_bidirectional_connection(converter: ConnectionConverter, sql_connection):
    class MockPlanet():
        def __init__(self, coords="A2"):
            self.coordinates = Coordinate.from_hex(coords)

    planet_1 = MockPlanet("A2")
    planet_2 = MockPlanet("B2")
    expected_first_query = f"DELETE FROM planetary_connections WHERE start_hex='A2' AND end_hex='B2'"
    expected_secondary_query = f"DELETE FROM planetary_connections WHERE start_hex='B2' AND end_hex='A2'"

    converter.delete_bidirectional_connection(planet_1, planet_2)
    queries = sql_connection.get_queries()
    assert strip_whitespace(queries[0]) == strip_whitespace(
        expected_first_query)
    assert strip_whitespace(queries[1]) == strip_whitespace(
        expected_secondary_query)

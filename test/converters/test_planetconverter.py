#! /usr/bin/env python3
import pytest
from swn_database.converters import PlanetConverter
from swn_database.data import Planet


@pytest.fixture
def converter(sql_connection):
    return PlanetConverter(sql_connection)


@pytest.fixture
def planet():
    return MockPlanet()


class MockPlanet():
    def __init__(self):
        self.ID = 20
        self.name = "mockplanet"
        self.coordinates = None
        self.tl = None
        self.biosphere = None
        self.atmosphere = None
        self.temperature = None
        self.population = None
        self.description = None

    def deserialize(self, serialized):
        pass


def strip_whitespace(string):
    return ''.join(string.split())


def test_create_table_query_ReturnsExpectedQuery(converter: PlanetConverter):
    expected_query = """
            CREATE TABLE IF NOT EXISTS planets (
                planet_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                coordinate TEXT,
                tl INTEGER,
                biosphere INTEGER,
                atmosphere INTEGER,
                temperature INTEGER,
                population INTEGER,
                description TEXT
            );
            """
    assert strip_whitespace(
        converter.create_table_query) == strip_whitespace(expected_query)


ADD_TEST_DATA = [
    (("A2", None), "('mockplanet', 'A2', NULL, NULL, NULL, NULL, NULL, NULL);"),
    ((None, None), "('mockplanet', NULL, NULL, NULL, NULL, NULL, NULL, NULL);"),
    (("A2", "Desc"), "('mockplanet', 'A2', NULL, NULL, NULL, NULL, NULL, 'Desc');"),
    ((None, "Desc"), "('mockplanet', NULL, NULL, NULL, NULL, NULL, NULL, 'Desc');")
]


@pytest.mark.parametrize("add_args, add_values", ADD_TEST_DATA)
def test_add_addsCorrectEntry(add_args, add_values, converter: PlanetConverter, sql_connection, monkeypatch):
    sql_connection.set_execute_read_results([False, [("deserialized")]])
    with monkeypatch.context() as m:
        m.setattr(Planet, "deserialize", lambda n: n)
        returned = converter.add_or_update(
            name="mockplanet",
            coords=add_args[0],
            tl=None,
            bio=None,
            atmos=None,
            temp=None,
            pop=None,
            desc=add_args[1])
    find_query = "SELECT planet_id FROM planets WHERE name='mockplanet'"
    add_query = """INSERT INTO planets (
            name, 
            coordinate, 
            tl, 
            biosphere, 
            atmosphere, 
            temperature, 
            population, 
            description)
        VALUES """ + add_values + "SELECT * FROM planets WHERE name='mockplanet'"

    queries = sql_connection.get_queries()

    assert strip_whitespace(find_query) == strip_whitespace(queries[0])
    assert strip_whitespace(add_query) == strip_whitespace(queries[1])
    assert returned == "deserialized"


def test_add_returnsNoneIfFailsToAdd(converter: PlanetConverter, sql_connection):
    sql_connection.set_execute_read_results([False, None])
    returned = converter.add_or_update("mockplanet")
    assert returned == None

def test_update_planet_executesCorrectQuery(converter: PlanetConverter, sql_connection, planet, monkeypatch):
    sql_connection.set_execute_read_results([["deserialized",]])

    update_query = """UPDATE planets 
        SET
            description='desc'
        WHERE
            name = 'mockplanet';
        SELECT * FROM planets WHERE name='mockplanet'"""
    planet.description = "desc"

    with monkeypatch.context() as m:
        m.setattr(Planet, "deserialize", lambda n: n)
        returned = converter.update_planet(planet)

    queries = sql_connection.get_queries()

    assert strip_whitespace(update_query) == strip_whitespace(queries[0])
    assert returned == "deserialized"

def test_update_returnsNoneIfNoValuesToUpdate(converter: PlanetConverter):
    returned = converter.update("mockplanet")
    assert returned == None


def test_update_returnsNoneIfFailsToUpdate(converter: PlanetConverter, sql_connection):
    sql_connection.set_execute_read_results([True, None])
    returned = converter.add_or_update("mockplanet", desc="description")
    assert returned == None


def test_delete_deletes(converter: PlanetConverter, sql_connection):
    planet = MockPlanet()
    converter.delete(planet)
    queries = sql_connection.get_queries()
    delete_query = queries[0]
    expected_query = f"DELETE FROM planets WHERE planet_id = {planet.ID}"
    assert strip_whitespace(expected_query) == strip_whitespace(delete_query)


def test_load_by_id_loads(converter: PlanetConverter, sql_connection, planet, monkeypatch):
    sql_connection.set_execute_read_results([planet])
    with monkeypatch.context() as m:
        m.setattr(Planet, "deserialize", lambda n: n)
        returned = converter.load_by_id(planet.ID)

    expected_query = f"SELECT * FROM planets WHERE planet_id = {planet.ID}"
    queries = sql_connection.get_queries()
    load_query = queries[0]

    assert returned == planet
    assert load_query == expected_query


def test_check_exists_returnsTrueIfIdIsFound(converter: PlanetConverter, sql_connection):
    sql_connection.set_execute_read_results([2])
    name = "test planet"
    expected_query = "SELECT planet_id FROM planets WHERE name='test planet'"

    result = converter.check_exists(name)

    find_query = sql_connection.get_queries()[0]

    assert result
    assert strip_whitespace(find_query) == strip_whitespace(expected_query)


def test_check_exists_returnsFalseIfNoIdFound(converter: PlanetConverter, sql_connection):
    sql_connection.set_execute_read_results([None])
    name = "test planet"
    expected_query = "SELECT planet_id FROM planets WHERE name='test planet'"

    result = converter.check_exists(name)

    find_query = sql_connection.get_queries()[0]

    assert not result
    assert strip_whitespace(find_query) == strip_whitespace(expected_query)


def test_load_by_name_loads(converter: PlanetConverter, sql_connection, planet, monkeypatch):
    sql_connection.set_execute_read_results([planet])
    with monkeypatch.context() as m:
        m.setattr(Planet, "deserialize", lambda n: n)
        returned = converter.load_by_name(planet.name)

    expected_query = f"SELECT * FROM planets WHERE name = {planet.name}"
    queries = sql_connection.get_queries()
    load_query = queries[0]
    assert returned == planet
    assert load_query == expected_query


def test_load_all_loads(converter: PlanetConverter, sql_connection, planet, monkeypatch):
    sql_connection.set_execute_read_results([[planet]])
    with monkeypatch.context() as m:
        m.setattr(Planet, "deserialize", lambda n: n)
        returned = converter.load_all()

    expected_query = f"SELECT * FROM planets"
    queries = sql_connection.get_queries()
    load_query = queries[0]
    assert returned == [planet]
    assert load_query == expected_query

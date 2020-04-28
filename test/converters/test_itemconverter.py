#! /usr/bin/env python3
import pytest
from swn_database.converters import ItemConverter
from swn_database.data import Item


@pytest.fixture
def converter(sql_connection):
    return ItemConverter(sql_connection)


@pytest.fixture
def item():
    return MockItem()


def strip_whitespace(string):
    return ''.join(string.split())


class MockItem(object):
    def __init__(self, ID=1, name="test", cost=2, enc=3, tl=4, packable=False):
        self.ID = ID
        self.name = name
        self.cost = cost
        self.enc = enc
        self.tl = tl
        self.packable = packable


def test_create_table_query_ReturnsExpectedQuery(converter: ItemConverter):
    expected_query = """
            CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            cost INTEGER NOT NULL,
            enc INTEGER NOT NULL,
            tl INTEGER NOT NULL,
            packable BIT NOT NULL
            );
            """
    assert strip_whitespace(
        converter.create_table_query) == strip_whitespace(expected_query)


def test_add_or_update_item_AddsItemIfNotExists(converter: ItemConverter, sql_connection, item, monkeypatch):
    NAME = "TEST"
    COST = 2
    ENC = 3
    TL = 4
    PACKABLE = True
    sql_connection.set_execute_read_results(
        [None, [(1, NAME, COST, ENC, TL, PACKABLE)]])
    with monkeypatch.context() as m:
        m.setattr("swn_database.data.Item", MockItem)
        returned_item = converter.add_or_update_item(
            NAME, COST, ENC, TL, PACKABLE)

    find_query = f"SELECT id FROM items WHERE name='{NAME}'"
    queries = sql_connection.get_queries()
    assert strip_whitespace(find_query) == strip_whitespace(queries[0])

    assert returned_item.name == NAME
    assert returned_item.cost == COST
    assert returned_item.encumbrance == ENC
    assert returned_item.tl == TL
    assert returned_item.packable == PACKABLE


def test_add_or_update_item_DoesNotAddIfMissingParameter(converter: ItemConverter, sql_connection, item, monkeypatch):
    NAME = "TEST"
    COST = 2
    ENC = 3
    TL = None
    PACKABLE = True
    sql_connection.set_execute_read_results([None, None])
    with monkeypatch.context() as m:
        m.setattr("swn_database.data.Item", MockItem)
        returned_item = converter.add_or_update_item(
            NAME, COST, ENC, TL, PACKABLE)

    find_query = f"SELECT id FROM items WHERE name='{NAME}'"
    queries = sql_connection.get_queries()
    assert strip_whitespace(find_query) == strip_whitespace(queries[0])

    assert returned_item is None


UPDATE_TEST_DATA = [
    (("TEST", 2, 3, 4, True),
     "UPDATE items SET cost=2 enc=3 tl=4 packable=1 WHERE name='TEST';"),
    (("TEST", None, 3, 4, True),
     "UPDATE items SET enc=3 tl=4 packable=1 WHERE name='TEST';"),
    (("TEST", 2, None, 4, True),
     "UPDATE items SET cost=2 tl=4 packable=1 WHERE name='TEST';"),
    (("TEST", 2, 3, None, True),
     "UPDATE items SET cost=2 enc=3 packable=1 WHERE name='TEST';"),
    (("TEST", 2, 3, 4, None), "UPDATE items SET cost=2 enc=3 tl=4 WHERE name='TEST';"),
    (("TEST", None, None, None, None), "")
]


@pytest.mark.parametrize("update_args, update_query", UPDATE_TEST_DATA)
def test_add_or_update_item_UpdatesItemIfExists(update_args, update_query, converter: ItemConverter, sql_connection, item, monkeypatch):
    NAME = "TEST"
    COST = 2
    ENC = 3
    TL = 4
    PACKABLE = True
    sql_connection.set_execute_read_results(
        [1, [(1, NAME, COST, ENC, TL, PACKABLE)]])
    with monkeypatch.context() as m:
        m.setattr(Item, "deserialize", lambda n: n)
        returned_item = converter.add_or_update_item(
            update_args[0], update_args[1], update_args[2], update_args[3], update_args[4])

    find_query = f"SELECT id FROM items WHERE name='{NAME}'"
    queries = sql_connection.get_queries()
    assert strip_whitespace(find_query) == strip_whitespace(queries[0])
    assert strip_whitespace(update_query + f"SELECT * FROM items WHERE name='{NAME}'") == strip_whitespace(queries[1])
    assert returned_item == (1, NAME, COST, ENC, TL, PACKABLE)


def test_delete_item_deletes_item(converter: ItemConverter, sql_connection, item):
    converter.delete_item(item)
    queries = sql_connection.get_queries()
    delete_query = queries[0]
    expected_query = f"DELETE FROM items WHERE id = {item.ID}"
    assert strip_whitespace(expected_query) == strip_whitespace(delete_query)


def test_load_item_by_id_loadsItem(converter: ItemConverter, sql_connection, item, monkeypatch):
    sql_connection.set_execute_read_results([item])

    with monkeypatch.context() as m:
        m.setattr(Item, "deserialize", lambda n: n)
        returned_item = converter.load_item_by_id(item.ID)

    expected_query = f"SELECT * FROM items WHERE id = {item.ID}"
    queries = sql_connection.get_queries()
    load_query = queries[0]

    assert returned_item == item
    assert strip_whitespace(expected_query) == strip_whitespace(load_query)


def test_get_all_items_getsAllItems(converter: ItemConverter, sql_connection, item, monkeypatch):
    sql_connection.set_execute_read_results([[item]])

    with monkeypatch.context() as m:
        m.setattr(Item, "deserialize", lambda n: n)
        returned_item = converter.get_all_items()

    expected_query = "SELECT * FROM items"
    queries = sql_connection.get_queries()
    load_query = queries[0]

    assert returned_item == [item]
    assert strip_whitespace(expected_query) == strip_whitespace(load_query)

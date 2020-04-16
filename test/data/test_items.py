#! /usr/bin/env python3
import pytest
from swn_database.data import Item, MeleeWeapon, RangedWeapon


def test_item_serialize_returnsExpectedString():
    expected_string = "0000000001100002030TestItem"

    item = Item(name="TestItem", ID=1, cost=20, packable=True, enc=3, tl=0)
    serialized_string = item.serialize()
    assert serialized_string == expected_string


def test_item_deserialize_returnsExpectedItem():
    serialized_item = "0000000001100002030TestItem"
    expected_item = Item(name="TestItem", ID=1, cost=20,
                         packable=True, enc=3, tl=0)

    deserialized_item = Item.deserialize(serialized_item)
    assert deserialized_item == expected_item


ITEM_EQUALITY_TESTDATA = [
    (("TestItem", 1), ("TestItem", 1), True),
    (("TestItem", 1), ("TestItem", 2), False),
    (("TestItem", 1), ("TestIten", 1), False),
]


@pytest.mark.parametrize("item1props,item2props,expected", ITEM_EQUALITY_TESTDATA)
def test_item_equality_shouldReturnExpectedResult(item1props, item2props, expected):
    item1 = Item(name=item1props[0], ID=item1props[1])
    item2 = Item(name=item2props[0], ID=item2props[1])

    equality = item1 == item2
    assert equality == expected


def test_item_equality_shouldReturnFalseIfNotComparedWithItem():
    class Mock_Equatable():
        def serialize(self):
            return "0000000001100002030TestItem"

    item = Item(name="TestItem", ID=1, cost=20, packable=True, enc=3, tl=0)

    assert (item == Mock_Equatable()) == False

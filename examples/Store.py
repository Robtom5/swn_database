#! /usr/bin/env python3
from swn_database.data import Item
from swn_database import SQLDatabaseLink
from swn_database.converters import ItemConverter


def print_item(item: Item):
    tick = u"\u2713"
    cross = u"\u2717"
    pound = "#"
    empty = ""
    print(f"{item.name:<15}\t{item.cost:>6}\t{item.encumbrance:>5}"
          + f"{pound if item.packable else empty}\t{item.tl:>2}")


if __name__ == "__main__":
    link = SQLDatabaseLink("./demo.db")
    converter = ItemConverter(link)
    link.connect()
    try:

        link.execute_query(converter.create_table_query)

        converter.add_or_update_item('Box', 5, 1, 1, False)
        converter.add_or_update_item('Roll of Tape', 15, 1, 2, True)
        converter.add_or_update_item('Chewing Gum', 1, 0, 3, False)
        converter.add_or_update_item('Bandaid', 10, 0, 3, True)

        converter.add_or_update_item('Box', cost=10)

        StoreItems = []
        items = link.execute_read_query("SELECT * from items")
        for item in items:
            StoreItems.append(Item.deserialize(item))

        print(f"{'Item':<15}\t{'Cost':>6}\t{'Enc':>6}\t{'TL':>2}")
        for item in StoreItems:
            print_item(item)

        print('\n---\nTL >= 2\n---')
        PackableItems = []
        p_items = link.execute_read_query("SELECT * from items WHERE tl >= 2")
        for item in p_items:
            PackableItems.append(Item.deserialize(item))
        for item in PackableItems:
            print_item(item)

    finally:
        link.close()

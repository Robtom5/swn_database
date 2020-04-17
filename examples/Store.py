#! /usr/bin/env python3
from swn_database.data import Item
from swn_database import SQLDatabaseLink


def print_item(item: Item):
    tick = u"\u2713"
    cross = u"\u2717"
    pound = "#"
    empty = ""
    # print(f"{item.Name:<15}\t{item.Cost:>6}\t{item.Encumbrance:>5}\t{tick if item.Packable else cross:^8}")
    print(f"{item.Name:<15}\t{item.Cost:>6}\t{item.Encumbrance:>5}{pound if item.Packable else empty}\t{item.TL:>2}")


if __name__ == "__main__":
    link = SQLDatabaseLink("./store.sqlite")
    link.connect()
    try:
        link.execute_query("""
            CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cost INTEGER NOT NULL,
            enc INTEGER NOT NULL,
            tl INTEGER NOT NULL,
            packable BIT NOT NULL
            );
            """)

        link.execute_query("""
            INSERT INTO
                items (id, name, cost, enc, tl, packable)
            VALUES
                (1, 'Box', 5, 1, 1, 0),
                (2, 'Roll of Tape', 15, 1, 2, 1),
                (3, 'Chewing Gum', 1, 0, 3, 0)
            """)

        StoreItems = []
        items = link.execute_read_query("SELECT * from items")
        for item in items:
            StoreItems.append(Item.deserialize(item))

        #link.execute_query("DROP TABLE items")


       # populate_store_items(StoreItems)
        # print(f"{'Item':<15}\t{'Cost':>6}\t{'Enc':>5}\t{'Packable':<8}")
        print(f"{'Item':<15}\t{'Cost':>6}\t{'Enc':>5}\t{'TL':>2}")
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

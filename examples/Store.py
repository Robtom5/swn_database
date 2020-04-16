#! /usr/bin/env python3
from swn_database.data import Item


def print_item(item: Item):
    tick = u"\u2713"
    cross = u"\u2717"
    print(f"{item.Name:<15}\t{item.Cost:>6}\t{item.Encumbrance:>5}\t{tick if item.Packable else cross:^8}")


def populate_store_items(itemlist: list):
    itemlist.append(Item(ID=1, name="Box", cost="5", enc=1, tl=1, packable=False))
    itemlist.append(Item(ID=2, name="Roll of Tape", cost="5", enc=1, tl=2, packable=True))
    itemlist.append(Item(ID=2, name="Chewing Gum", cost="5", enc=0, tl=2, packable=False))



if __name__ == "__main__":
    StoreItems = []

    populate_store_items(StoreItems)
    print(f"{'Item':<15}\t{'Cost':>6}\t{'Enc':>5}\t{'Packable':<8}")
    for item in StoreItems:
        print_item(item)

#! /usr/bin/env python3
from swn_database.data import Planet, Coordinate
from swn_database import SQLDatabaseLink
from swn_database.converters import PlanetConverter

def print_planet(planet):
    print(f"{planet.coordinates} - {planet.name:<3}")

if __name__ == "__main__":
    link = SQLDatabaseLink("./demo.db")
    converter = PlanetConverter(link)
    link.connect()
    try:
        # link.execute_query("DROP TABLE planets")
        link.execute_query(converter.create_table_query)
        converter.add(
            name="Planet A",
            coords=Coordinate.from_hex('B2'))
        converter.add(
            name="Planet B",
            coords=Coordinate.from_hex('B4'))
        converter.add(
            name="Planet C",
            coords=Coordinate.from_hex('A4'))
        converter.add(
            name="Planet D",
            coords=Coordinate.from_hex('A5'))

        planet_items = converter.load_all()

        for planet in planet_items:
            print_planet(planet)
    finally:
        link.close()

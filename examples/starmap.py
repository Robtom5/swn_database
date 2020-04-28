#! /usr/bin/env python3
from swn_database.data import Planet, Coordinate, Connection
from swn_database import SQLDatabaseLink
from swn_database.converters import PlanetConverter, ConnectionConverter

def print_planet(planet):
    print(f"{planet.coordinates} - {planet.name:<3}")

if __name__ == "__main__":
    link = SQLDatabaseLink("./demo.db")
    planet_converter = PlanetConverter(link)
    conn_converter = ConnectionConverter(link)
    link.connect()
    try:
        link.execute_query("DROP TABLE planets")
        link.execute_query("DROP TABLE planetary_connections")
        link.execute_query(planet_converter.create_table_query)
        link.execute_query(conn_converter.create_table_query)
        planet1 = planet_converter.add(
            name="Planet A",
            coords=Coordinate.from_hex('B2'))
        planet2 = planet_converter.add(
            name="Planet B",
            coords=Coordinate.from_hex('B4'))
        planet3 = planet_converter.add(
            name="Planet C",
            coords=Coordinate.from_hex('A4'))
        planet4 = planet_converter.add(
            name="Planet D",
            coords=Coordinate.from_hex('A5'))

        conn_converter.create_bidirectional_connection(planet1, planet2)
        conn_converter.create_bidirectional_connection(planet2, planet3)
        conn_converter.create_bidirectional_connection(planet2, planet4)
        conn_converter.create_bidirectional_connection(planet3, planet4)

        planet_items = planet_converter.load_all()
        connections = conn_converter.load_all()

        for planet in planet_items:
            print_planet(planet)

        # for conn in connections:
        #     print(conn)

        linked = link.execute_read_query("""
            SELECT name FROM planets
            WHERE coordinate IN (
                SELECT
                    end_hex
                FROM
                    planetary_connections
                WHERE
                    start_hex='B4'
            )
            """)
        print("Planet B connects to: " + ", ".join([l[0] for l in linked]))
       
    finally:
        link.close()

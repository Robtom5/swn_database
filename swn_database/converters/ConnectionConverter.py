#! /usr/bin/env python3
from ..data import Connection, Coordinate
from .PlanetConverter import PlanetConverter
from ..SQLDatabaseLink import SQLDatabaseLink


class ConnectionConverter():
    def __init__(self, link: SQLDatabaseLink):
        self.sql_link = link

    @property
    def table_name(self):
        return "planetary_connections"

    @property
    def create_table_query(self):
        return f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                start_hex TEXT NOT NULL,
                end_hex TEXT NOT NULL,
                connection_id INTEGER PRIMARY KEY AUTOINCREMENT,
                UNIQUE(start_hex, end_hex)
            );
            """

    def add(self, start_hex, end_hex):
        query = f"""
            INSERT INTO {self.table_name} (
                start_hex,
                end_hex
            ) VALUES (
                '{start_hex}',
                '{end_hex}'
            );
            SELECT * FROM {self.table_name} 
            WHERE start_hex='{start_hex}' AND end_hex='{end_hex}'"""
        new_entry = self.sql_link.execute_read_query(query)
        if new_entry:
            start, end, conn_id = new_entry[0]
            return Connection(start_hex=Coordinate.from_hex(start), end_hex=Coordinate.from_hex(end), conn_id=conn_id)
        else:
            return None

    def update():
        pass

    def delete():
        pass

    def load_by_id(self, connection_id: int):
        start_raw, end_raw, conn_id = self.sql_link.execute_read_query(f"SELECT * FROM {self.table_name} WHERE id = {connection_id}")
        start_hex = Coordinate.from_hex(start_raw)
        end_hex = Coordinate.from_hex(end_raw)
        return Connection(start_hex=start_hex, end_hex=end_hex, conn_id=conn_id)

    def load_all(self):
        return [Connection(start_hex=Coordinate.from_hex(start), end_hex=Coordinate.from_hex(end), conn_id=conn_id) for start, end, conn_id in self.sql_link.execute_read_query(f"SELECT * FROM {self.table_name}")]

    def create_bidirectional_connection(self, planet_1, planet_2):
        self.add(planet_1.coordinates, planet_2.coordinates)
        self.add(planet_2.coordinates, planet_1.coordinates)
        pass

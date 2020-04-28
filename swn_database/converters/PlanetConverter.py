#! /usr/bin/env python3
from ..data import Planet
from ..SQLDatabaseLink import SQLDatabaseLink
from ..data import Coordinate


class PlanetConverter():
    def __init__(self, link: SQLDatabaseLink):
        self.sql_link = link

    @property
    def table_name(self):
        return "planets"

    @property
    def create_table_query(self):
        return f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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

    def add(self,
            name: str,
            coords: Coordinate = None,
            tl: int = None,
            bio: int = None,
            atmos: int = None,
            temp: int = None,
            pop: int = None,
            desc: str = None
            ):

        query = f"""
            INSERT INTO
                {self.table_name} (
                    name, 
                    coordinate, 
                    tl, 
                    biosphere, 
                    atmosphere, 
                    temperature, 
                    population, 
                    description)""" + f"""
            VALUES
                (
                    '{name}',
                    {f"'{coords}'" if coords is not None else "NULL"},
                    {tl},
                    {bio},
                    {atmos},
                    {temp},
                    {pop}, """.replace("None", "NULL") + f"""
                    {f"'{desc}'" if desc is not None else "NULL"}
                    );
                    """
        updated_entry = self.sql_link.execute_read_query(
            query + f"SELECT * FROM {self.table_name} WHERE name='{name}'")
        if updated_entry:
            return Planet.deserialize(updated_entry[0])
        else:
            return None

    def update(self,
               name: str,
               coords: Coordinate = None,
               tl: int = None,
               bio: int = None,
               atmos: int = None,
               temp: int = None,
               pop: int = None,
               desc: str = None
               ):
        if not all(arg is None for arg in [coords, tl, bio, atmos, temp, pop, desc]):
            query = f"""
                UPDATE
                    {self.table_name}
                SET
                    {f"coordinate='{coords}'" if coords is not None else ""}
                    {f"tl={tl}" if tl is not None else ""}
                    {f"biosphere={bio}" if bio is not None else ""}
                    {f"atmosphere={atmos}" if atmos is not None else ""}
                    {f"temperature={temp}" if temp is not None else ""}
                    {f"population={pop}" if pop is not None else ""}
                    {f"description='{desc}'" if desc is not None else ""}
                WHERE
                    name = '{name}';
            """
            new_entry = self.sql_link.execute_read_query(
                query + f"SELECT * FROM {self.table_name} WHERE name='{name}'")
            if new_entry:
                return Planet.deserialize(new_entry[0])
            else:
                return None
        else:
            return None

    def update_planet(self, planet: Planet):
        return self.update(
            name = planet.name,
            coords = planet.coordinates,
            tl = planet.tl,
            bio = planet.biosphere,
            atmos = planet.atmosphere,
            temp = planet.temperature,
            pop = planet.population,
            desc = planet.description)

    def add_or_update(self,
                      name: str,
                      coords: Coordinate = None,
                      tl: int = None,
                      bio: int = None,
                      atmos: int = None,
                      temp: int = None,
                      pop: int = None,
                      desc: str = None
                      ):
        if self.check_exists(name):
            return self.update(name, coords, tl, bio, atmos, temp, pop, desc)
        else:
            return self.add(name, coords, tl, bio, atmos, temp, pop, desc)

    def delete(self,
               planet: Planet):
        self.sql_link.execute_query(f"""
            DELETE FROM {self.table_name}
            WHERE id = {planet.ID}
            """)

    def check_exists(self, name):
        exists = False
        existing_entry = self.sql_link.execute_read_query(f"""
            SELECT
                id
            FROM
                {self.table_name}
            WHERE
                name='{name}'
            """)
        if existing_entry:
            exists = True

        return exists

    def load_by_id(self, ID):
        query_res = self.sql_link.execute_read_query(f"SELECT * FROM {self.table_name} WHERE id = {ID}")
        return Planet.deserialize(query_res)

    def load_by_name(self, name):
        query_res = self.sql_link.execute_read_query(f"SELECT * FROM {self.table_name} WHERE name = {name}")
        return Planet.deserialize(query_res)

    def load_all(self):
        return [Planet.deserialize(res) for res in self.sql_link.execute_read_query(f"SELECT * FROM {self.table_name}")]

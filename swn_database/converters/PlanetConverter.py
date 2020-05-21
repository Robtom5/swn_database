#! /usr/bin/env python3
from ..data import Planet
from ..SQLDatabaseLink import SQLDatabaseLink
from ..data import Coordinate


class PlanetConverter():
    def __init__(self, link: SQLDatabaseLink):
        self.sql_link = link

    table_name="planets"

    create_table_query="""
            CREATE TABLE IF NOT EXISTS planets (
                planet_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                coordinate TEXT,
                tl INTEGER,
                biosphere INTEGER,
                atmosphere INTEGER,
                temperature INTEGER,
                population INTEGER,
                description TEXT,
                notes TEXT
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
            desc: str = None,
            notes: str = None
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
                    description,
                    notes)""" + f"""
            VALUES
                (
                    '{name}',
                    {f"'{coords}'" if coords is not None else "NULL"},
                    {tl},
                    {bio},
                    {atmos},
                    {temp},
                    {pop}, """.replace("None", "NULL") + f"""
                    {f"'{desc}'," if desc is not None else "NULL,"}
                    {f"'{notes}'" if notes is not None else "NULL"}
                    );
                    """
        new_entry = self.sql_link.execute_read_query(
            query + f"SELECT * FROM {self.table_name} WHERE name='{name}'")
        if new_entry:
            self.sql_link.commit()
            return Planet.deserialize(new_entry[0])
        else:
            self.sql_link.rollback()
            return None

    def update(self,
               name: str,
               coords: Coordinate = None,
               tl: int = None,
               bio: int = None,
               atmos: int = None,
               temp: int = None,
               pop: int = None,
               desc: str = None,
               notes: str = None
               ):
        if not all(arg is None for arg in [coords, tl, bio, atmos, temp, pop, desc, notes]):
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
                    {f"notes='{notes}'" if notes is not None else ""}
                WHERE
                    name = '{name}';
            """
            new_entry = self.sql_link.execute_read_query(
                query + f"SELECT * FROM {self.table_name} WHERE name='{name}'")
            if new_entry:
                self.sql_link.commit()
                return Planet.deserialize(new_entry[0])
            else:
                self.sql_link.rollback()
                return None
        else:
            return None

    def update_planet(self, planet: Planet):
        return self.update(
            name=planet.name,
            coords=planet.coordinates,
            tl=planet.tl,
            bio=planet.biosphere,
            atmos=planet.atmosphere,
            temp=planet.temperature,
            pop=planet.population,
            desc=planet.description,
            notes=planet.notes)

    def add_or_update(self,
                      name: str,
                      coords: Coordinate = None,
                      tl: int = None,
                      bio: int = None,
                      atmos: int = None,
                      temp: int = None,
                      pop: int = None,
                      desc: str = None,
                      notes: str = None
                      ):
        if self.check_exists(name):
            return self.update(name, coords, tl, bio, atmos, temp, pop, desc, notes)
        else:
            return self.add(name, coords, tl, bio, atmos, temp, pop, desc, notes)

    def delete(self,
               planet: Planet):
        self.sql_link.execute_query(f"""
            DELETE FROM {self.table_name}
            WHERE planet_id = {planet.ID}
            """)
        self.sql_link.commit()

    def check_exists(self, name):
        exists = False
        existing_entry = self.sql_link.execute_read_query(f"""
            SELECT
                planet_id
            FROM
                {self.table_name}
            WHERE
                name='{name}'
            """)
        if existing_entry:
            exists = True

        return exists

    def get_planet_name(self, ID):
        query_res = self.sql_link.execute_read_query(
            f"SELECT name FROM {self.table_name} WHERE planet_id = {ID}",
            suppress=True)
        return query_res[0][0] if query_res else None

    def load_by_id(self, ID):
        query_res = self.sql_link.execute_read_query(
            f"SELECT * FROM {self.table_name} WHERE planet_id = {ID}")
        return Planet.deserialize(query_res[0])

    def load_by_name(self, name):
        query_res = self.sql_link.execute_read_query(
            f"SELECT * FROM {self.table_name} WHERE name = '{name}'")
        if query_res:
            return Planet.deserialize(query_res[0])
        else:
            return None

    def load_all(self, order=None):
        query = f"SELECT * FROM {self.table_name}"
        if order is not None:
            ordering = f" ORDER BY {order} ASC"
            query = query + ordering
        return [Planet.deserialize(res) for res in self.sql_link.execute_read_query(query)]

    def available_planets(self):
        return self.sql_link.execute_read_query(f"SELECT name FROM {self.table_name}")

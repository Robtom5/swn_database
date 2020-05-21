#! /usr/bin/env python3
from ..data import Character
from ..factories import CharacterFactory
from ..SQLDatabaseLink import SQLDatabaseLink
from .PlanetConverter import PlanetConverter


class CharacterConverter():
    def __init__(self, link: SQLDatabaseLink, character_factory: CharacterFactory):
        self.sql_link = link
        self.character_factory = character_factory

    table_name = "characters"

    create_table_query = """
            CREATE TABLE IF NOT EXISTS characters (
                character_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                age INTEGER,
                homeworld INTEGER,
                curr_world INTEGER,
                description TEXT,
                notes TEXT,
                trustworthiness INTEGER,
                desire TEXT,
                isPC BIT NOT NULL DEFAULT 0,
                role TEXT,
                UNIQUE(name, surname),
                FOREIGN KEY (homeworld) REFERENCES planets (planet_id)
                    ON DELETE RESTRICT
                    ON UPDATE NO ACTION,
                FOREIGN KEY (curr_world) REFERENCES planets (planet_id)
                    ON DELETE SET NULL
                    ON UPDATE NO ACTION
            );
            """

    def create_character(self, name, surname, isPC):
        query = f"""
            INSERT INTO {self.table_name} (name, surname, isPC)
            VALUES
            (
                '{name}',
                '{surname}',
                {int(isPC)}
            );
        """
        new_entry = self.sql_link.execute_read_query(
            query + f"SELECT * FROM {self.table_name} WHERE name='{name}'")
        if new_entry:
            self.sql_link.commit()
            return self.character_factory.create(new_entry[0])
        else:
            self.sql_link.rollback()
            return None

    def update_character(self, character: Character):
        if character is not None:
            query = f"""
                UPDATE
                    {self.table_name}
                SET
                    name='{character.name}',
                    surname='{character.surname}',
                    age={character.age},
                    homeworld={character.homeworld},
                    curr_world={character.current_planet},
                    trustworthiness={character.trustworthiness},
                    isPC={int(character.isPC)},""".replace("None", "NULL") + f"""
                    role='{character.role}',
                    description='{character.description}',
                    notes='{character.notes}',
                    desire='{character.desire}'
                WHERE
                    character_id={character.ID};
            """.replace("'None'", "NULL")
            new_entry = self.sql_link.execute_read_query(
                query + f"""
                    SELECT * FROM {self.table_name}
                    WHERE character_id='{character.ID}'""")
            if new_entry:
                self.sql_link.commit()
                return self.character_factory.create(new_entry[0])
            else:
                self.sql_link.rollback()
                return None
        else:
            return None

    def load_by_id(self, character_id):
        serialized = self.sql_link.execute_read_query(f"""
            SELECT * FROM {self.table_name}
            WHERE character_id={character_id}
            """)
        if serialized:
            return self.character_factory.create(serialized[0])
        else:
            return None

    def load_by_name(self, name, surname):
        # try and load
        character_id = self.sql_link.execute_read_query(f"""
            SELECT character_id
            FROM {self.table_name}
            WHERE name='{name}' AND surname='{surname}'
            """)
        if character_id:
            return self.load_by_id(character_id[0][0])
        else:
            return None

    def available_names(self):
        return [(n, s) for n, s in self.sql_link.execute_read_query(f"""
            SELECT name, surname FROM {self.table_name}
            ORDER BY isPC, name, surname ASC
            """)]

    def load_all(self, id):
        pass

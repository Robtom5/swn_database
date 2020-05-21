#! /usr/bin/env python3

from swn_database import SQLDatabaseLink
from swn_database.converters import PlanetConverter, ConnectionConverter, OpinionConverter, CharacterConverter


def initialize_database(link: SQLDatabaseLink):
    link.connect()
    link.execute_query(PlanetConverter(link=None).create_table_query)
    link.execute_query(ConnectionConverter(link=None).create_table_query)
    link.execute_query(CharacterConverter.create_table_query)
    link.execute_query(OpinionConverter.create_table_query)


if __name__ == "__main__":
    link = SQLDatabaseLink("./system.db")
    try:
        initialize_database(link)
        # link.execute_query("""
        #     PRAGMA foreign_keys=off;
        #     BEGIN TRANSACTION;
        #     CREATE TABLE IF NOT EXISTS chartemp(
        #         character_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         name TEXT NOT NULL,
        #         surname TEXT NOT NULL,
        #         age INTEGER,
        #         homeworld INTEGER,
        #         curr_world INTEGER,
        #         description TEXT,
        #         notes TEXT,
        #         trustworthiness INTEGER,
        #         desire TEXT,
        #         isPC BIT NOT NULL DEFAULT 0,
        #         UNIQUE(name, surname),
        #         FOREIGN KEY (homeworld) REFERENCES planets (planet_id)
        #             ON DELETE RESTRICT
        #             ON UPDATE NO ACTION,
        #         FOREIGN KEY (curr_world) REFERENCES planets (planet_id)
        #             ON DELETE SET NULL
        #             ON UPDATE NO ACTION
        #     );
        #     INSERT INTO chartemp(character_id, name, surname, age, homeworld, curr_world, isPC)
        #     SELECT character_id, name, surname, age, homeworld, curr_world, isPC
        #     FROM characters;

        #     DROP TABLE characters;
        #     ALTER TABLE chartemp RENAME TO characters;
        #     COMMIT;

        #     PRAGMA foreign_keys=on;
        #     """)
        [print(table) for table in link.execute_read_query("""
            SELECT 
                name
            FROM 
                sqlite_master 
            WHERE 
                type ='table' AND 
                name NOT LIKE 'sqlite_%'
        """)]
    finally:
        link.close()

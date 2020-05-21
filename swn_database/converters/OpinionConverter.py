#! /usr/bin/env python3

from ..SQLDatabaseLink import SQLDatabaseLink
from ..factories import OpinionFactory


class OpinionConverter():
    def __init__(self, link: SQLDatabaseLink, opinion_factory: OpinionFactory):
        self.sql_link = link
        self.opinion_factory = opinion_factory

    table_name="opinions"

    create_table_query="""
            CREATE TABLE IF NOT EXISTS opinions (
                character_id INTEGER NOT NULL,
                target_id INTEGER NOT NULL,
                opinion INTEGER DEFAULT 50,
                PRIMARY KEY (character_id, target_id),
                FOREIGN KEY (character_id) REFERENCES characters (character_id)
                    ON DELETE RESTRICT
                    ON UPDATE NO ACTION,
                FOREIGN KEY (target_id) REFERENCES characters (character_id)
                    ON DELETE RESTRICT
                    ON UPDATE NO ACTION
            );
            """

    def create_opinion(self, char_id, targ_id):
        query = f"""
        INSERT INTO {self.table_name}(character_id, target_id)
        VALUES ({char_id}, {targ_id});
        SELECT * FROM {self.table_name}
        WHERE character_id={char_id} AND target_id={char_id}
        """
        res = self.sql_link.execute_read_query(query)
        if res:
            return self.opinion_factory.create(res[0])
        else:
            return None

    def modify_opinion(self, character, target, value=50):
        query = f"""
        UPDATE {self.table_name}
        SET opinion={value}
        WHERE character_id={character.ID} AND target_id={target.ID};
        SELECT * FROM {self.table_name}
        WHERE character_id={character.ID} AND target_id={target.ID}
        """
        if not self.load_opinion(character.ID, target.ID):
            self.create_opinion(character.ID, target.ID)

        opinion = self.sql_link.execute_read_query(query)
        if opinion:
            self.sql_link.commit()
            return self.opinion_factory.create(opinion[0])
        else:
            self.sql_link.rollback()
            return None

    def load_opinion(self, char_id, targ_id):
        query = f"""SELECT * FROM {self.table_name} WHERE
            character_id={char_id} AND target_id={targ_id}"""
        res = self.sql_link.execute_read_query(query)
        if res:
            return self.opinion_factory.create(res[0])
        else:
            return None

    def delete_opinion(self, char_id, targ_id):
        self.sql_link.execute_query(f"""
            DELETE FROM {self.table_name}
            WHERE character_id={char_id}
            AND target_id={targ_id}
            """)
        self.sql_link.commit()

#! /usr/bin/env python3
from ..data import Item
from ..SQLDatabaseLink import SQLDatabaseLink


class ItemConverter():
    def __init__(self, link: SQLDatabaseLink):
        self.sql_link = link

    @property
    def create_table_query(self):
        return f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            cost INTEGER NOT NULL,
            enc INTEGER NOT NULL,
            tl INTEGER NOT NULL,
            packable BIT NOT NULL
            );
            """

    @property
    def table_name(self):
        return "items"

    def add_or_update_item(self,
                           name: str,
                           cost: int = None,
                           enc: int = None,
                           tl: int = None,
                           packable: bool = None):
        existing_entry = self.sql_link.execute_read_query(f"""
            SELECT 
                id
            FROM
                {self.table_name} 
            WHERE
                name='{name}'
            """)
        query = ""
        if existing_entry:
            if not all(arg is None for arg in [cost, enc, tl, packable]):
                query = f"""
                    UPDATE
                        {self.table_name} 
                    SET
                        {f"cost={cost}" if cost is not None else ""}
                        {f"enc={enc}" if enc is not None else ""}
                        {f"tl={tl}" if tl is not None else ""}
                        {f"packable={int(packable)}" if packable is not None else ""}
                    WHERE
                        name = '{name}';
                    """
        else:
            if not any(arg is None for arg in [cost, enc, tl, packable]):
                query = f"""
                    INSERT INTO
                        {self.table_name} (name, cost, enc, tl, packable)
                    VALUES
                        ('{name}', {cost}, {enc}, {tl}, {int(packable)});                
                    """

        updated_entry = self.sql_link.execute_read_query(
            query + f"SELECT * FROM {self.table_name} WHERE name='{name}'")

        if updated_entry:
            return Item.deserialize(updated_entry[0])
        else:
            return None

    def delete_item(self, existing_item: Item):
        self.sql_link.execute_query(f"""
            DELETE FROM {self.table_name} 
            WHERE id = {existing_item.ID}
            """)

    def load_item_by_id(self, id):
        query_res = self.sql_link.execute_read_query(f"SELECT * FROM {self.table_name} WHERE id ={id}")
        return Item.deserialize(query_res)

    def get_all_items(self):
        return [Item.deserialize(res) for res in self.sql_link.execute_read_query(f"SELECT * FROM {self.table_name}")]

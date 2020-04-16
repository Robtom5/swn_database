#! /usr/bin/env python3
import sqlite3


class SQLDatabaseLink(object):
    def __init__(self, database_path):
        self._Database_Path = database_path
        self.Connection = None

    @property
    def Database_Path(self):
        return self._Database_Path

    def connect(self):
        self.close()
        try:
            self.Connection = sqlite3.connect(self.Database_Path)
            print("Connection to SQLite DB successful")
        except sqlite3.Error as e:
            print(f"The error '{e}' occured")

    def close(self):
        if self.Connection is not None:
            self.Connection.close()
            self.Connection = None

    def execute_query(self, query, verbose=False):
        if self.Connection is None:
            raise Error("Must connect to database first")
        cursor = self.Connection.cursor()
        try:
            cursor.execute(query)
            self.Connection.commit()
            if verbose:
                print("Query executed successfully")
        except sqlite3.Error as e:
            print(f"The error '{e}' occured")

    def execute_read_query(self, query):
        if self.Connection is None:
            raise Error("Must connect to database first")
        cursor = self.Connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"The error '{e}' occured")


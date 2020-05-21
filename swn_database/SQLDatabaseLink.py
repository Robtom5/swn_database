#! /usr/bin/env python3
import sqlite3


class SQLDatabaseLink(object):
    def __init__(self, database_path):
        self._database_path = database_path
        self.conn = None

    @property
    def database_path(self):
        return self._database_path

    def connect(self):
        self.close()
        try:
            self.conn = sqlite3.connect(self.database_path)
            print("Connection to SQLite DB successful")
        except sqlite3.Error as e:
            print(f"The error '{e}' occured")

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def execute_query(self, query, verbose=False, suppress=False):
        if self.conn is None:
            raise Exception("Must connect to database first")
        cursor = self.conn.cursor()
        try:
            cursor.executescript(query)
            self.conn.commit()
            if verbose:
                print("Query executed successfully")
        except sqlite3.Error as e:
            if not suppress:
                print(f"The error '{e}' occured")

    def execute_read_query(self, query, suppress=False):
        if self.conn is None:
            raise Exception("Must connect to database first")
        cursor = self.conn.cursor()
        result = None
        try:
            for subquery in query.split(";"):
                cursor.execute(subquery)
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            if not suppress:
                print(f"The error '{e}' occured")

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

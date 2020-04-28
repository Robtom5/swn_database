#! /usr/bin/env python3
import sqlite3
from .DataStructures import Coordinate


class Connection():
    def __init__(self,
                 *,
                 start_hex: Coordinate,
                 end_hex: Coordinate,
                 conn_id: int,
                 **kwargs):
        super().__init__(**kwargs)
        self._start_hex = start_hex
        self._end_hex = end_hex
        self._connection_id = conn_id

    @property
    def start_hex(self):
        return self._start_hex

    @property
    def end_hex(self):
        return self._end_hex

    @property
    def connection_id(self):
        return self._connection_id
    
    def __eq__(self, other):
        """Override of equality comparison"""
        if isinstance(other, Connection):
            return other.serialize() == self.serialize()
        return False

    def serialize(self) -> tuple:
        """Serialize an instance of the class as a string"""
        return (f"{self.start_hex}", f"{self.end_hex}", self.connection_id)

    def __str__(self):
        return f"{self.start_hex} -> {self.end_hex}"
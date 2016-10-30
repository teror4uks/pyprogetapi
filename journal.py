import sqlite3


class Journal:

    def __init__(self):
        self.db = sqlite3.connect(':memory:')
        self.db.executescript(
            'create table packages("")'

        )

    def insert_packs(self):

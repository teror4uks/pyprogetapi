import sqlite3


class Journal:

    def __init__(self):
        self.db = sqlite3.connect(':memory:')
        self.db.execute(
            'create table packages (pack_id, version)'
        )

    def insert_packs(self, walker):
        for w in walker:
            self.db.execute("insert into packages (pack_id, version) VALUES (:Package_Id, :Version_Text)", w)
            # print(w)

    def show_table(self):
        for row in self.db.execute('select * from packages'):
            print(row)


import sqlite3

class DataOperator:

    def __init__(self, db_name="./data.db"):
        self.db_name = db_name

    def make_connection(self):
        connection = sqlite3.connect(self.db_name)
        connection.execute("PRAGMA foreign_keys = ON;")
        return connection

    def make_table(self):
        connection = self.make_connection()
        cursor = connection.cursor()

        # Tworzy tablice uczniowie
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uczniowie (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                imie TEXT,
                nazwisko TEXT,
                klasa TEXT
                )
        """)

        # Tworzy tablice typy zajec
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS typyzajec (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            typ_zajec TEXT UNIQUE
            )             
        """)

        # Tworzy selectables z tej tablicy
        cursor.execute("SELECT COUNT(*) FROM typyzajec")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""INSERT INTO typyzajec(typ_zajec) VALUES
                 ("Przygotowanie do E8"),
                 ("Przygotowanie do Matury"),
                 ("Powtórki do zajęć"),
                 ("Nadrobienie zaległości"),
                 ("Inne")
                 """
                       )

        # Tworzy tablice zajecia
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS zajecia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_ucznia INTEGER,
                data_zajec TEXT,
                stawka REAL,
                id_typzajec INTEGER,
                FOREIGN KEY (id_ucznia) REFERENCES uczniowie (id),
                FOREIGN KEY (id_typzajec) REFERENCES typyzajec (id)
                )
        """)


        connection.commit()
        connection.close()
        print("Bazy danych utworzono.")

    def add_student(self, imie, nazwisko, klasa):
        connection = self.make_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO uczniowie(imie, nazwisko, klasa) VALUES (?,?,?) ", (imie, nazwisko, klasa))

        connection.commit()
        print("Dodano ucznia "+str(imie)+" "+str(nazwisko))

    def return_students(self):
        connection = self.make_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM uczniowie")
        connection.commit()
        return cursor.fetchall()

    def add_zajecia(self, id_ucznia, id_zajec, data_zajec, stawka):
        connection = self.make_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO zajecia(id_ucznia, id_typzajec, data_zajec, stawka) VALUES (?,?,?,?) ",(id_ucznia, id_zajec, data_zajec, stawka))
        connection.commit()

    def overall_zarobki(self):
        connection = self.make_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT ROUND(SUM(stawka),2) FROM zajecia")
        ret = cursor.fetchone()
        kwota = ret[0] or 0.0
        return kwota

    def showZajecia(self):
        connection = self.make_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT zajecia.id, zajecia.data_zajec, zajecia.stawka, typyzajec.typ_zajec, uczniowie.imie, uczniowie.nazwisko 
            FROM zajecia
            INNER JOIN typyzajec ON zajecia.id_typzajec = typyzajec.id 
            INNER JOIN uczniowie ON zajecia.id_ucznia = uczniowie.id
        """)
        connection.commit()
        return cursor.fetchall()
    

import os, sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        #testing if database directory exists
        if os.path.exists("database_folder"):
            pass
            if os.path.exists("database_folder/database.db"):
                pass
                if os.path.exists("database_folder/youth register files"):
                    pass
                else:
                    os.mkdir('database_folder/youth register files')
            else:
                conn = sqlite3.connect("database_folder/database.db")
                cur = conn.cursor()
                self.my_cursor(cur)
                conn.commit()
                cur.close()
                conn.close()
        else:
            # creating directory
            os.mkdir("database_folder")
            # changing cwd to database path
            os.chdir("database_folder")
            os.mkdir('youth register files')

            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            self.my_cursor(cur)
            conn.commit()
            cur.close()
            conn.close()


    def register_new_member(self, first_name=None,
                                  middle_name=None,
                                  last_name=None,
                                  fone_number=None,
                                  date=None,
                                  gender=None,
                                  address=None):
        conn = sqlite3.connect("database_folder/database.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO members(name,middle,surname,cellfone,dob,gender,address) VALUES (?,?,?,?,?,?,?)",
                                        (first_name, middle_name,last_name, fone_number, date, gender,address))
        conn.commit()
        cur.close()
        conn.close()


    def register_new_user(self, name=None,surname=None,title=None,pwd=None):
        conn = sqlite3.connect("database_folder/database.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO users(name,surname,title,password) VALUES (?,?,?,?)",
                                        (name, surname, title, pwd))
        conn.commit()
        cur.close()
        conn.close()

    def inventory_update(self,item=None, description=None,state=None):
        conn = sqlite3.connect("database_folder/database.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO inventory(item,description,state) VALUES (?,?,?)",(item,description,state))
        conn.commit()
        cur.close()
        conn.close()

    def my_cursor(self, cur):
        # creating a new database if it doesnt exist
        '''Each value stored in an SQLite database (or manipulated by the database engine) has one of the following storage classes:
           NULL.    The value is a NULL value.
           INTEGER. The value is a signed integer, stored in 1, 2, 3, 4, 6, or 8 bytes depending on the magnitude of the value.
           REAL.    The value is a floating point value, stored as an 8-byte IEEE floating point number.
           TEXT.    The value is a text string, stored using the database encoding (UTF-8, UTF-16BE or UTF-16LE).
           BLOB.    The value is a blob of data, stored exactly as it was input.
        '''
        cur.execute("CREATE TABLE IF NOT EXISTS members(name TEXT, middle TEXT, surname TEXT, cellfone TEXT, dob TEXT, gender TEXT, address TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS sunday_register(register_date BLOB,adults TEXT,children TEXT,visitors TEXT,attendance TEXT,notes TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS church_programs(date BLOB, name TEXT, contact_person TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS evens(event_date BLOB, title TEXT, venue TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, surname TEXT, title TEXT, password TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS inventory(item TEXT, description TEXT, state TEXT)")
        cur.execute("INSERT INTO users(name, surname,title,password) VALUES (?,?,?,?)",
                                        ('1', 'NULL', 'NULL', '1'))


class CreateNewYouth:
    def __init__(self, name=None, surname=None, age=None, favorites=None):
        self.name = name
        self.surname = surname
        self.age = age
        self.favorites = favorites
        filename = self.name+ " " +self.surname
        with open(f"database_folder/youth register files/{filename}.txt", 'w') as file:
            file.write(f"Name : {self.name} {self.surname}\n")
            file.write(f"Registered date : {datetime.now()}\n")
            file.write(f"Age : {self.age}\n")
            file.write(f"Favorites : {self.favorites}\n")

class MainServiceRegister:
    def __init__(self,date=None,adults=None,children=None,visitors=None, attendance=None,notes=None):
        attendance = int(adults) + int(children) + int(visitors)
        with open('database_folder/data.txt', 'a') as file:
            file.write(f"{date},{attendance}"+"\n")
        print(date)
        print(adults)
        print(children)
        print(visitors)
        print(attendance)
        print(notes)
        conn = sqlite3.connect("database_folder/database.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO sunday_register(register_date,adults, children,visitors,attendance,notes) VALUES (?,?,?,?,?,?)",
                                       (date, adults,children,visitors,attendance,notes))
        conn.commit()
        cur.close()
        conn.close()

class Register:
    def __init__(self, name=None,attend=None):
        for i in os.listdir('database_folder/youth register files/.'):
            if name == i.split('.')[0]:
                with open(f"database_folder/youth register files/{i}", 'a') as file:
                    file.write(f"{datetime.now().strftime('%H:%M:%S %d-%m-%Y')} {attend}\n")

class delete_entry:
    def __init__(self, name=None):
        pass



       

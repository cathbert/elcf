import os, sqlite3

class User_Login:
    def login_user(username,password):
        try:
            conn = sqlite3.connect("database_folder/database.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM users")

            for user in cur.fetchall():
                if user[0] == username and user[-1] == password:
                    return True
                    

            cur.close()


        except Exception as e:
            print('Error', str(e))

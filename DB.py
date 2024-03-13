from flask_mysqldb import MySQL

mysql = None  # mysql 인스턴스 초기화

def init_db(app):
    global mysql
    mysql = MySQL(app)

def insert_user(name, email, hashed_password):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
            mysql.connection.commit()
        return True
    except Exception as e:
        print(f"DB Insert Error: {e}")
        mysql.connection.rollback()
        return False

def get_user_by_email(email):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT id, name, email, password FROM users WHERE email=%s", (email,))
            return cursor.fetchone()
    except Exception as e:
        print(f"DB Query Error: {e}")
        return None

def get_user_by_userid(user_id):
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT id, name, email, password FROM users WHERE id=%s",(user_id,))
            return cursor.fetchone()
    except Exception as e:
        print(f"DB Query Error: {e}")
        return None

        
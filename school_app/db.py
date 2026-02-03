import pymysql

def db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Ds@270705",
        database="school_management",
        cursorclass=pymysql.cursors.DictCursor
    )
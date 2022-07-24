import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    # create a database connection to the SQLite database
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    # create a table from the create_table_sql statement
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit
        
    except Error as e:
        print(e)


def main():
    database =r".\database\Users.db"

    sql_create_accounts_table = """ CREATE TABLE IF NOT EXISTS ACCOUNTS (
                                        id integer PRIMARY KEY AUTOINCREMENT ,
                                        username text NOT NULL,
                                        password text NOT NULL,
                                        email text NOT NULL
                                    ); """

    sql_create_certificate_table = """CREATE TABLE IF NOT EXISTS CERTIFICATE (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    user_id integer NOT NULL,
                                    image_name text NOT NULL,
                                    descraption text ,
                                    FOREIGN KEY (user_id) REFERENCES ACCOUNTS (id)
                                );"""

    sql_create_user_infos_table = """CREATE TABLE IF NOT EXISTS user_infos (
                                    id	INTEGER PRIMARY KEY AUTOINCREMENT,
	                                user_id	INTEGER NOT NULL,
                                    firstname	TEXT,
                                    lastname	TEXT,
                                    mobile_number	TEXT,
                                    address_line1	TEXT,
                                    address_line2	TEXT,
                                    postcode	TEXT,
                                    state	TEXT,
                                    area	TEXT,
                                    education	TEXT,
                                    country	TEXT,
                                    Experience	TEXT,
                                    additional_details	TEXT,
                                    FOREIGN KEY (user_id) REFERENCES ACCOUNTS (id)
                                );"""
    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create accounts table
        create_table(conn, sql_create_accounts_table)

        # create certificate table
        create_table(conn, sql_create_certificate_table)

        # create user_infos table
        create_table(conn, sql_create_user_infos_table)
        conn.commit
        conn.close
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
     main()
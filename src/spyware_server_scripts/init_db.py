import os, json
import psycopg2 as pg

# Get Config data from file specified in argv and verify it
def get_config (*args):
    default_config_file = "./config.json"
    config_file = args[0] if len(args) > 0 else None
    
    if config_file is None and not os.path.exists(default_config_file) :
        print ("[ERROR] config file not specified and default file doesn't exists")
        print (f"[*] please, create config file {default_config_file} or specify your file as an argument")
        return None
    elif config_file is None :
        config_file = default_config_file
    elif config_file is not None and not os.path.exists(default_config_file) :
        print ("[ERROR] the config file specified doesn't exists")
        return None

    config_file_stream = open(config_file)
    config = json.loads(config_file_stream.read())
    config_file_stream.close()

    if 'db' not in config :
        print ("[ERROR] db field is not in config file")
        return None
    
    return config

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
        id UUID PRIMARY KEY default uuid_generate_v4(),
        os_name VARCHAR NOT NULL,
        os_version_release VARCHAR NOT NULL,
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

    # cursor.close()
    connection.close()
import psycopg2 as pg

from spyware_server_common.config import get_config
from spyware_server_common.utils import hashStr

def create_access (cursor, username, password) :
    sql_statement = 'INSERT INTO access (username, password) VALUES (%s, %s);'
    
    try :
        cursor.execute(sql_statement, (username, password))
        cursor.connection.commit()
    except pg.errors.UniqueViolation :
        print(f"[ERROR] the username {username} already exists.")
        return
    except Exception as ex :
        print("[ERROR]", ex.__str__())
        return
    
    print ("[*] Access created")

def add_access (*args) :
    config = None

    if len(args) < 2 :
        print ("[ERROR] too few arguments")
        print ("[USAGE] spyware_server_scripts add_access [config_file:optional] [username] [password]" )
        return
    
    if len (args) == 2 : config = get_config()
    else : config = get_config(*args)

    username = args[1]
    password = args[2]

    connection = pg.connect(**config["db"])
    cursor = connection.cursor()

    create_access(cursor, username, hashStr(password))
    
    cursor.close()
    connection.close()


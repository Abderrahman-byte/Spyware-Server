def get_access_by_username (cursor, username) :
    try :
        sql_statement = 'SELECT username,password,active FROM access WHERE username = %s'
        cursor.execute(sql_statement,(username,))
        data = cursor.fetchone()
    except Exception as ex:
        print('[ERROR] get_access_by_username : ' + ex.__str__())
        return None

    if data is None : return None
    
    return {
        'username': data[0],
        'password': data[1],
        'active': data[2]
    }
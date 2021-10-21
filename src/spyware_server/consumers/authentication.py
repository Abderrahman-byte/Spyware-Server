import json
import jwt

from spyware_server_common.utils import checkHash
from spyware_server_common.config import get_config

from ..models.access import get_access_by_username


def validate_authentication_message (data) :
    required = ["username", "password"]

    for required_field in required :
        if required_field not in data :
            return False

    return True

def send_rpc_error_reply (ch, method, properties, error_title) :
    return_payload = json.dumps({ 'error': error_title })
    ch.basic_publish(exchange='', routing_key=properties.reply_to, body=return_payload)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def send_rpc_reply (ch, method, properties, body) :
    ch.basic_publish(exchange='', routing_key=properties.reply_to, body=body)
    ch.basic_ack(delivery_tag=method.delivery_tag)  

def create_authentication_callback (cursor) :
    def callback (ch, method, properties, body) :
        data = None
        config = get_config()

        try :
            data = json.loads(body.decode())
        except :
            send_rpc_error_reply(ch, method, properties, 'invalid_body')
            return  

        if not validate_authentication_message(data) :
            send_rpc_error_reply(ch, method, properties, 'invalid_schema')
            return 

        username = data['username']
        password = data['password']

        access_data = get_access_by_username(cursor, username)

        if access_data is None or not checkHash(access_data['password'], password):
            send_rpc_error_reply(ch, method, properties, 'invalid_credentials')
            return

        token = jwt.encode({'username': username}, config.get('secrect', '123456'))
        return_payload = json.dumps({ 'token': token })
        send_rpc_reply (ch, method, properties, return_payload)

    return callback

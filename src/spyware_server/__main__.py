import pika, psycopg2 as pg

from spyware_server_common.config import get_config
from .consumers.authentication import create_authentication_callback
from .amqp import openAmqpConnection, initQueues

def main () :
    config = get_config("./config.json")
    rmqConfig = config["rmq"]

    pgConnection = pg.connect(**config['db'])
    pgCursor = pgConnection.cursor()
    amqpConnection = openAmqpConnection(rmqConfig)
    mainChannel = amqpConnection.channel()
    
    initQueues(amqpConnection)

    mainChannel.basic_qos(prefetch_count=1)
    mainChannel.basic_consume('auth', create_authentication_callback(pgCursor))

    mainChannel.start_consuming()

if __name__ == '__main__' :
    main()
import pika

from spyware_server_common.config import get_config
from .amqp import openAmqpConnection, initQueues

def main () :
    config = get_config("./config.json")
    rmqConfig = config["rmq"]

    amqpConnection = openAmqpConnection(rmqConfig)
    initQueues(amqpConnection)

if __name__ == '__main__' :
    main()
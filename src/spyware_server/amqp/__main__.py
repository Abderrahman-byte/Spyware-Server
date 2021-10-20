import pika

def openAmqpConnection (config) :
    pikaCredentails = pika.PlainCredentials(config['user'], config['password'])
    pikaParameters = pika.ConnectionParameters(host=config['host'], virtual_host=config['vhost'], credentials=pikaCredentails)
    return pika.BlockingConnection(pikaParameters)

def initQueues (connection) :
    queues = ['auth', 'keylogging']
    channel = connection.channel()
    args = {'x-queue-mode': 'lazy'}

    for queue in queues :
        channel.queue_declare(queue=queue, durable=True, arguments=args)
        print(f'[*] Queue "{queue}" has been created')

    channel.close()
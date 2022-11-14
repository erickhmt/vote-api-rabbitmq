
import json
import pika

print(' [*] Connecting to rabbitmq server')
#These credentials should preferably be stored in environment variables, I will leave it here for study purposes
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange='votes', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='votes', queue=queue_name)

print(' [*] Waiting for messages')

def callback(ch, method, properties, body):
    print(" [x] Received %s" % body)
    reqObj = json.loads(body)
    print(" [x] Voted on %d" % reqObj['vote'])

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
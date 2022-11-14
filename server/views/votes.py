from flask import Blueprint
from flask import request
import pika
import json

bp_votes = Blueprint('votes', __name__, url_prefix='/votes')

@bp_votes.route("/", methods=["POST"])
def vote():
    requestObj = request.json
    print(requestObj)

    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange='votes', exchange_type='fanout')

    message = json.dumps(requestObj)
    channel.basic_publish(exchange='votes', routing_key='', body=message)
    connection.close()

    response = {'status': 'Request created', 'message': message}, 201
    return response

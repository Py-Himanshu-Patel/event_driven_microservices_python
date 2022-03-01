import json
import pika
credentials = pika.PlainCredentials("admin", "admin")
# name of container and host port on which AMQP is available this connection is 
# possible only if both request making container and request accepting container 
# are connected to same network here it is admin_default which is the network
# got created with docker compose of admin app
params = pika.ConnectionParameters(host="rabbitmq", port=5672, credentials=credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish(method, body):
	properties = pika.BasicProperties(method)
	channel.basic_publish(
		exchange='', 
		routing_key='main', 
		body=json.dumps(body),
		properties=properties
	)

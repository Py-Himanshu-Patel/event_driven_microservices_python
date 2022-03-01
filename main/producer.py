import pika, json

credentials = pika.PlainCredentials("admin", "admin")	# username password
params = pika.ConnectionParameters(
	host="rabbitmq", 
	port=5672, 
	credentials=credentials
)
connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish(method, body):
	properties = pika.BaseConnection(method)
	channel.basic_publish(
		exchange='', 
		routing_key='admin',
		body=json.dumps(body),
		properties=properties
		)

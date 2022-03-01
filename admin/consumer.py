import django, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'admin.settings'
django.setup()

import pika, json
from products.models import Product

credentials = pika.PlainCredentials("admin", "admin")	# username password
params = pika.ConnectionParameters(
	host="rabbitmq", 
	port=5672, 
	credentials=credentials
)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
	print('Received in admin')
	id = json.loads(body)
	product = Product.objects.filter(id=id)
	if not product.exists():
		print(f"Product do not exist {id}")
	product = product.first()
	product.likes += 1
	product.save()
	print("Product likes increased !!")

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print("Started Consuming")
channel.start_consuming()
channel.close()

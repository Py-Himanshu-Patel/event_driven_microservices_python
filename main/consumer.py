import pika, json
from main import Product, db

credentials = pika.PlainCredentials("admin", "admin")	# username password
params = pika.ConnectionParameters(
	host="rabbitmq", 
	port=5672, 
	credentials=credentials
)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Received in main')
    data = json.loads(body)
    action = data.get('action')
    print(data)

    if action == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('Product Created')

    elif action == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print('Product Updated')

    elif action == 'product_deleted':
        product = Product.query.get(data.get("pk"))
        db.session.delete(product)
        db.session.commit()
        print('Product Deleted')

    else:
        print(f"This action not handeled: {action}")


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')
channel.start_consuming()
channel.close()

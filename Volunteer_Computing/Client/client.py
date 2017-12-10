import os
import pika

def get_task():
	os.system("curl http://localhost:5000/mac > task")
	os.system("chmod +x task")
	return

def get_data():
	os.system("curl http://localhost:5000/data > data.txt")
	return

def execute():
	os.system("./task data.txt")

def main():
	get_task()
	get_data()
	execute()
	return

def dequeue():
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.queue_declare(queue='hello')

	def callback(ch, method, properties, body):
	    print(" [x] Received %r" % body)

	channel.basic_consume(callback,queue='hello',no_ack=True)

	print(' [*] Waiting for messages. To exit press CTRL+C')
	channel.start_consuming()
	return

def subscribe():
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.exchange_declare(exchange='tasks',exchange_type='fanout')

	queue = channel.queue_declare(exclusive=True)
	queue_name = queue.method.queue
	channel.queue_bind(exchange='tasks',queue = queue_name)

	print(' [*] Waiting for tasks. To exit press CTRL+C')

	def callback(ch, method, properties, body):
	    print(" [x] %r" % body)

	channel.basic_consume(callback,queue=queue_name,no_ack=True)
	channel.start_consuming()

if __name__ == '__main__':
	subscribe()
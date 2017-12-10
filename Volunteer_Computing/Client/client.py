import os
import pika

def get_task():
	os.system("curl http://localhost:5000/mac > task")
	os.system("chmod +x task")
	return

def get_data(no):
	os.system("curl http://localhost:5000/data/"+str(no)+" > data"+str(no)+".txt")
	return

def execute(no):
	os.system("./task data"+str(no)+".txt")

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
	    # print(" [x] %r" % body)
	    get_task()
	    # os.system("curl http:/localhost:5000/"+body.split('_')[1])
	    return

	channel.basic_consume(callback,queue=queue_name,no_ack=True)
	channel.start_consuming()
	return

def get_work():
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.queue_declare(queue='data',durable=True)
	print(' [*] Waiting for data. To exit press CTRL+C')

	def callback(ch, method, properties, body):
	    print(" [x] Received %r" % body)
	    
	    data_id = int(body)
	    get_data(data_id)
	    execute(data_id)

	    print(" [x] Done")
	    ch.basic_ack(delivery_tag = method.delivery_tag)

	channel.basic_qos(prefetch_count=1)
	channel.basic_consume(callback,queue='data')

	channel.start_consuming()
	return


if __name__ == '__main__':
	get_work()
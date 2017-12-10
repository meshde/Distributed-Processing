import os
import io
from flask import Flask
from flask import send_file
import pika
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)


@app.route('/')
def hello():
	return "Hello World!\n"

@app.route('/mac')
def get_task():
	path = os.path.join(BASE,'matrix_mac')
	with open(path,'rb') as file:
		return send_file(io.BytesIO(file.read()),mimetype='application/octet-stream',attachment_filename='matrix')

@app.route('/data/<int:no>')
def get_data(no):
	return send_file('data'+str(no)+'.txt',attachment_filename='data.txt',mimetype='text/plain')

@app.route('/enqueue')
def enqueue():
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.queue_declare(queue='hello')

	channel.basic_publish(exchange='',
	                      routing_key='hello',
	                      body='Hello World!')
	print(" [x] Sent 'Hello World!'")
	connection.close()
	return "OK\n"

@app.route('/assign')
def assign_task():
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.exchange_declare(exchange='tasks',exchange_type='fanout')
	message = "matrix_mac"

	channel.basic_publish(exchange='tasks',routing_key='',body=message)
	print(" [x] Sent %r" % message)

	connection.close()
	return "OK\n"

@app.route('/assign/data')
def assign_data():
	n = 5
	create_data(n)
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.queue_declare(queue='data', durable=True)
	for i in range(1,n+1):
		channel.basic_publish(exchange='',routing_key='data',body=str(i),properties=pika.BasicProperties(delivery_mode=2))
		print(" [x] Sent %d" % i)

	connection.close()
	return "OK\n"

def create_data(n):
	a = np.random.randint(11,size=(n,n))
	b = np.random.randint(11,size=(n,n))

	for i in range(n):
		with open("data"+str(i+1)+".txt",'w') as f:
			f.write(str(n)+"\n")
			for j in range(n-1):
				f.write(str(a[i][j])+" ")
			f.write(str(a[i][n-1])+"\n")
			for j in range(n-1):
				f.write(str(b[j][i])+" ")
			f.write(str(b[n-1][i])+"\n")
	return

def main():
	app.run(debug=True)
	return

if __name__ == '__main__':
	main()
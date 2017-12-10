import os
import io
from flask import Flask
from flask import send_file
import pika

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

@app.route('/data')
def get_data():
	return send_file('hello.txt',attachment_filename='data.txt',mimetype='text/plain')

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

def main():
	app.run(debug=True)
	return

if __name__ == '__main__':
	main()
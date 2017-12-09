import os
import io
from flask import Flask
from flask import send_file

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

def main():
	app.run(debug=True)
	return

if __name__ == '__main__':
	main()
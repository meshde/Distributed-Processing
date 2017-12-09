import os

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

if __name__ == '__main__':
	main()
import socket

class SocketClient():

	connection = None

	HOST = '127.0.0.1'
	PORT = 7777

	def __init__(self):
		self.init(self.HOST, self.PORT)

	def init(self, host: str, port: str) -> None:
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			self.connection.connect((host, int(port)))
			self.loop()
		except socket.error as error:
			print(error)
			self.connection = None

	def loop(self) -> None:
		try:
			while (True):
				message = self.read()
				if (message == ''):
					break
				print(message[2:])
		except KeyboardInterrupt:
			self.connection.close()

	def read(self) -> str:
		return self.connection.recv(4096).decode('utf-8')

	def send(self, data: str) -> None:
		self.connection.send(bytes(data, 'utf-8'))

SocketClient()
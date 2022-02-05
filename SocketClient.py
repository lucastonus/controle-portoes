import sys
import socket

class SocketClient():

	connection = None

	def __init__(self, host: str, port: int):
		self.init(host, port)

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
				print(message)
		except KeyboardInterrupt:
			self.connection.close()

	def read(self) -> str:
		return self.connection.recv(4096).decode('utf-8')

	def send(self, data: str) -> None:
		self.connection.send(bytes(data, 'utf-8'))

if __name__ == "__main__":
	if (len(sys.argv) == 3):
		SocketClient(sys.argv[1], sys.argv[2])
	else:
		print('Formato inválido: [host] [port]')
import json
import socket
import threading
import gatesAPI

class SocketServer:

	running = False
	connection = None

	client = None
	address = None

	def __init__(self, host: str, port: int):
		self.init(host, port)

	def init(self, host: str, port: int):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			print(f'Servidor iniciado em [{host}:{port}], aguardando conexões.')
			self.connection.bind((host, port))
			self.connection.listen()
		except socket.error as msg:
			print(f'Erro ao iniciar servidor: {msg}')
			self.connection = None

	def run(self):
		self.running = True

		while self.running:
			client, address = self.connection.accept()

			if (self.client != None):
				self.stopClient()

			threading._start_new_thread(self.newClient, (client, address))

		self.connection.close()

	def newClient(self, client, address):
		self.client = client
		self.address = address

		print(f'Conexão estabelecida: {address}')
		gatesAPI.init(self)

	def stopClient(self):
		print(f'Conexão encerrada: {self.address}')
		self.client.close()

	def stop(self):
		if (self.client != None):
			self.stopClient()

		self.running = False
		print('Servidor encerrado.')

	def sendMessage(self, payload):
		if (self.client != None):
			self.client.sendall(bytearray([1, 125]) + bytes(json.dumps(payload), 'utf-8'))
			return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
		else:
			return json.dumps({'success': False}), 404, {'ContentType': 'application/json'}

if __name__ == '__main__':
	socketServer = SocketServer('', 8888)
	socketServer.run()
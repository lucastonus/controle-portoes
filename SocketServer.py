from DBConn import DBConn
import json
import socket
import threading

class SocketServer:

	socket = None

	client = None
	clientAddress = None

	def init(self, host: str, port: int):
		if (self.socket == None):
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.settimeout(30)

			try:
				print(f'Servidor iniciado em [{host}:{port}], aguardando conexões.')
				self.socket.bind((host, port))
				self.socket.listen()
			except socket.error as msg:
				print(f'Erro ao iniciar servidor: {msg}')
				self.socket = None

		return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

	def acceptConnection(self):
		if (self.socket != None):
			self.stopClient()
			client, address = self.socket.accept()
			threading._start_new_thread(self.newClient, (client, address))
			return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
		else:
			return json.dumps({'success': False}), 503, {'ContentType': 'application/json'}

	def stop(self):
		self.stopClient()

		if (self.socket != None):
			self.socket.close()
			self.socket = None
			print('Servidor encerrado.')

		return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

	def newClient(self, client, address):
		self.client = client
		self.clientAddress = address
		print(f'Conexão estabelecida: {address}')

	def stopClient(self):
		if (self.client != None):
			print(f'Conexão encerrada: {self.clientAddress}')
			self.client.close()
			self.client = None

	def sendMessage(self, message: str):
		if (self.client != None):
			self.client.sendall(bytearray([1, 125]) + bytes(message, 'utf-8'))

	def openGates(self, payload: dict, idUser: int):
		if (self.client != None):
			if (len(payload['gates']['gate']) == 2):
				gate = 3
			else:
				if (payload['gates']['gate'][0] == 'GATE_INSIDE'):
					gate = 2
				else:
					gate = 1

			db = DBConn()
			db.insert("INSERT INTO log (id_user, gate) VALUES (%s, %s)", [idUser, gate])

			self.sendMessage(json.dumps(payload))
			return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
		else:
			return json.dumps({'success': False}), 503, {'ContentType': 'application/json'}